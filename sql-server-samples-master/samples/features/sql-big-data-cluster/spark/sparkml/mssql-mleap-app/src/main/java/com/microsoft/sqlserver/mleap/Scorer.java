package com.microsoft.sqlserver.mleap;

import com.microsoft.sqlserver.javalangextension.AbstractSqlServerExtensionExecutor;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.commons.cli.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.Reader;

import java.sql.JDBCType;
import java.sql.Types;

import java.util.Arrays;
import java.util.List;
import java.util.LinkedHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Scorer extends AbstractSqlServerExtensionExecutor {

    private static final Logger LOGGER = Logger.getLogger(Scorer.class.getName());

    public Scorer() {
        executorExtensionVersion = SQLSERVER_JAVA_LANG_EXTENSION_V1;
        executorInputDatasetClassName = PrimitiveDataset.class.getName();
        executorOutputDatasetClassName = PrimitiveDataset.class.getName();
    }

    public void init(String sessionId, int taskId, int numTasks) {
        System.out.println("init SessionID: " + sessionId + " taskId: " + taskId + " numTasks: " + numTasks);
    }

    public PrimitiveDataset execute(PrimitiveDataset input, LinkedHashMap<String, Object> params) {
        List<String> logLevels = Arrays.asList("OFF", "SEVERE", "WARNING", "INFO", "CONFIG", "FINE", "FINER", "FINEST", "ALL");
        String logLevel = params.getOrDefault("logLevel", "WARNING").toString();
        if (!logLevels.contains(logLevel)) {
            throw new IllegalArgumentException("logLevel (" + logLevel + ") must be one of " + logLevels.toString());
        }
        LOGGER.setLevel(Level.parse(logLevel));

        LOGGER.info("Logger Name: " + LOGGER.getName() + "; Logger Level:" + LOGGER.getLevel());

        // load model
        String modelPath;
        try {
            modelPath = params.get("modelPath").toString();
        } catch (NullPointerException e) {
            throw new IllegalArgumentException("modelPath parameter is required but not set.");
        }

        long startTime = System.nanoTime();
        Predictor scorer = new Predictor();
        scorer.init(modelPath);
        long endTime = System.nanoTime();
        long duration = (endTime - startTime);  //divide by 10^6 to get milliseconds.
        LOGGER.info("model loading time: " + duration/1e6 + " ms");

        // convert PrimitiveDataset to DefaultLeapFrame
        startTime = System.nanoTime();
        scorer.primitiveDataset2leapFrame(input);
        endTime = System.nanoTime();
        duration = (endTime - startTime);  //divide by 10^6 to get milliseconds.
        LOGGER.info("PrimitiveDataset to DefaultLeapFrame conversion time: " + duration/1e6 + " ms");

        // do prediction
        startTime = System.nanoTime();
        scorer.run();
        endTime = System.nanoTime();
        duration = (endTime - startTime);  //divide by 10^6 to get milliseconds.
        LOGGER.info("model scoring time: " + duration/1e6 + " ms");

        //select output fields specified
        startTime = System.nanoTime();
        String[] outputFields;
        outputFields = params.getOrDefault("outputFields", "").toString().split(",");
        scorer.select(outputFields);
        endTime = System.nanoTime();
        duration = (endTime - startTime);  //divide by 10^6 to get milliseconds.
        LOGGER.info("data selection time: " + duration/1e6 + " ms");

        // convert DefaultLeapFrame to PrimitiveDataset
        startTime = System.nanoTime();
        PrimitiveDataset output = new PrimitiveDataset();
        scorer.leapFrame2primitiveDataset(output);
        endTime = System.nanoTime();
        duration = (endTime - startTime);  //divide by 10^6 to get milliseconds.
        LOGGER.info("DefaultLeapFrame to PrimitiveDataset conversion time: " + duration/1e6 + " ms");

        return output;
    }

    public void cleanup() {
        System.out.println("\n* cleanup");
    }

    /**
     *
     * @param args commandline options for model path and input file.
     * @throws Exception
     * <pre>
     * {@code
     *
     * -- ex: Linux
     * java -cp mssql-mleap-app-assembly-1.0.jar:mssql_java_lang_extension.jar:mssql-mleap-lib-assembly-1.0.jar:commons-csv-1.5.jar:commons-cli-1.4.jar com.microsoft.sqlserver.mleap.Scorer
     *  -m /tmp/adult_census_pipeline.zip
     *  -i /tmp/adult_census_income.csv
     *
     * java -cp "*" -m /tmp/adult_census_pipeline.zip -i /tmp/adult_census_income.csv
     *
     * -- ex: Windows
     * java -cp mssql-mleap-app-assembly-1.0.jar;mssql_java_lang_extension.jar;mssql-mleap-lib-assembly-1.0.jar;commons-csv-1.5.jar:commons-cli-1.4.jar com.microsoft.sqlserver.mleap.Scorer
     *  -m C:\\Users\\lgong\\Work\\git\\aml-databricks\\examples\\mleapsql2\\src\\main\\resources\\sqlqueries\\adult_census_pipeline.zip
     *  -i C:\\Users\\lgong\\Work\\git\\aml-databricks\\examples\\mleapsql2\\src\\main\\resources\\sqlqueries\\adult_census_income.csv
     *
     * java -cp "*"
     *  -m C:\\Users\\lgong\\Work\\git\\aml-databricks\\examples\\mleapsql2\\src\\main\\resources\\sqlqueries\\adult_census_pipeline.zip
     *  -i C:\\Users\\lgong\\Work\\git\\aml-databricks\\examples\\mleapsql2\\src\\main\\resources\\sqlqueries\\adult_census_income.csv
     * }
     * </pre>
     */
    public static void main(String[] args) throws Exception {
        // get model and testing data
        Options options = new Options();

        Option input = new Option("i", "input", true, "input file");
        input.setRequired(true);
        options.addOption(input);

        Option model = new Option("m", "model", true, "model path");
        model.setRequired(true);
        options.addOption(model);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("Scorer", options);

            System.exit(1);
        }

        String modelPath = cmd.getOptionValue("model");
        String scoreFile = cmd.getOptionValue("input");

        LOGGER.info("os.name: " + System.getProperty("os.name"));
        LOGGER.info("isWindows: " + System.getProperty("os.name").startsWith("Windows"));
        LOGGER.info("args: " + Arrays.toString(args));

        LOGGER.info("modelPath: " + modelPath);
        LOGGER.info("scoreFile: " + scoreFile);

        // read in the testing data
        BufferedReader bufferedReader = new BufferedReader(new FileReader(scoreFile));
        int nRows = -1; //account for the header row
        while(bufferedReader.readLine() != null) {
            nRows++;
        }

        LinkedHashMap<String, Integer> inputFields = new LinkedHashMap<String, Integer>();
        inputFields.put("age", Types.INTEGER);
        inputFields.put("workclass", Types.NVARCHAR);
        inputFields.put("fnlwgt", Types.INTEGER);
        inputFields.put("education", Types.NVARCHAR);
        inputFields.put("education_num", Types.INTEGER);
        inputFields.put("marital_status", Types.NVARCHAR);
        inputFields.put("occupation", Types.NVARCHAR);
        inputFields.put("relationship", Types.NVARCHAR);
        inputFields.put("race", Types.NVARCHAR);
        inputFields.put("sex", Types.NVARCHAR);
        inputFields.put("capital_gain", Types.INTEGER);
        inputFields.put("capital_loss", Types.INTEGER);
        inputFields.put("hours_per_week", Types.INTEGER);
        inputFields.put("native_country", Types.NVARCHAR);
        inputFields.put("income", Types.NVARCHAR);

        String[] columnNames = {"age", "hours_per_week", "education", "sex", "income"}; //choose the input variables
        int[] columnTypes = new int[columnNames.length];
        for (int iCol = 0; iCol < columnNames.length; iCol++) {
            try {
                columnTypes[iCol] = inputFields.get(columnNames[iCol]);
            } catch (NullPointerException e) {
                throw new IllegalArgumentException("invalid input field: " + columnNames[iCol]);
            }
        }
        int nCols = columnNames.length;

        Object[] columns = new Object[nCols];
        for (int iCol = 0; iCol < nCols; iCol++) {
            int columnType = columnTypes[iCol];
            switch (columnType) {
                case Types.INTEGER:
                    columns[iCol] = new int[nRows];
                    break;
                case Types.NVARCHAR:
                    columns[iCol] = new String[nRows];
                    break;
                default:
                    throw new IllegalArgumentException("unsupported sql type: " + JDBCType.valueOf(columnType).getName());
            }
        }

        Reader in = new FileReader(scoreFile);
        Iterable<CSVRecord> records = CSVFormat.RFC4180.withFirstRecordAsHeader().parse(in);
        int iRow = 0;
        for (CSVRecord record : records) {
            for (int iCol = 0; iCol < nCols; iCol++) {
                int columnType = columnTypes[iCol];
                switch (columnType) {
                    case Types.INTEGER:
                        ((int[])(columns[iCol]))[iRow] = Integer.parseInt(record.get(columnNames[iCol]));
                        break;
                    case Types.NVARCHAR:
                        ((String[])(columns[iCol]))[iRow] = record.get(columnNames[iCol]);
                        break;
                    default:
                        throw new IllegalArgumentException("unsupported sql type: " + JDBCType.valueOf(columnType).getName());
                }
            }
            iRow++;
        }

        // form the primitive dataset
        PrimitiveDataset inputds = new PrimitiveDataset();

        for (int iCol = 0; iCol < nCols; iCol++) {
            int columnType = columnTypes[iCol];
            switch (columnType) {
                case Types.INTEGER:
                    inputds.addColumnMetadata(iCol, columnNames[iCol], Types.INTEGER, 0, 0);
                    inputds.addIntColumn(iCol, (int[])(columns[iCol]), null);
                    break;
                case Types.NVARCHAR:
                    inputds.addColumnMetadata(iCol, columnNames[iCol], Types.NVARCHAR, 0, 0);
                    inputds.addStringColumn(iCol, (String[])(columns[iCol]));
                    break;
                default:
                    throw new IllegalArgumentException("unsupported sql type: " + JDBCType.valueOf(columnType).getName());
            }
        }

        // specify some params
        LinkedHashMap<String, Object> params = new LinkedHashMap<>();
        params.put("logLevel", "INFO"); //default WARN
        params.put("modelPath", modelPath);
        params.put("outputFields", "prediction,probability,education,sex,income,predictedIncome");
        //params.put("outputFields", "features,education-encoded"); //SparseTensor

        // perform scoring
        Scorer scorer  = new Scorer();
        scorer.init("session0", 0, 1);
        PrimitiveDataset output = scorer.execute(inputds, params);

        // display output
        int nOutputCols = output.getColumnCount();
        System.out.println("\nnOutputCols: " + nOutputCols);

        for (int iCol = 0; iCol < nOutputCols; iCol++) {
            System.out.println("\nColumnName: " + output.getColumnName(iCol));

            int columnType = output.getColumnType(iCol);
            System.out.println("ColumnType: " + JDBCType.valueOf(columnType).getName());

            switch(columnType) {
                case Types.INTEGER:
                    int[] intColumn = output.getIntColumn(iCol);
                    System.out.println("Column.length: " + intColumn.length);
                    System.out.println("Column: " + Arrays.toString(intColumn));
                    break;
                case Types.DOUBLE:
                    double[] doubleColumn = output.getDoubleColumn(iCol);
                    System.out.println("Column.length: " + doubleColumn.length);
                    System.out.println("Column: " + Arrays.toString(doubleColumn));
                    break;
                case Types.BIGINT:
                    long[] longColumn = output.getLongColumn(iCol);
                    System.out.println("Column.length: " + longColumn.length);
                    System.out.println("Column: " + Arrays.toString(longColumn));
                    break;
                case Types.BIT:
                    boolean[] booleanColumn = output.getBooleanColumn(iCol);
                    System.out.println("Column.length: " + booleanColumn.length);
                    System.out.println("Column: " + Arrays.toString(booleanColumn));
                    break;
                case Types.FLOAT:
                    float[] floatColumn = output.getFloatColumn(iCol);
                    System.out.println("Column.length: " + floatColumn.length);
                    System.out.println("Column: " + Arrays.toString(floatColumn));
                    break;
                case Types.SMALLINT:
                    short[] shortColumn = output.getShortColumn(iCol);
                    System.out.println("Column.length: " + shortColumn.length);
                    System.out.println("Column: " + Arrays.toString(shortColumn));
                    break;
                case Types.NVARCHAR:
                    String[] stringColumn = output.getStringColumn(iCol);
                    System.out.println("Column.length: " + stringColumn.length);
                    System.out.println("Column: " + Arrays.toString(stringColumn));
                    break;
                default:
                    System.out.println("No columnType " + JDBCType.valueOf(columnType).getName());
            }
        }

        // cleanup
        scorer.cleanup();
    }
}
