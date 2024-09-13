package com.microsoft.sqlserver.mleap;

import org.junit.*;

import java.sql.Types;
import java.util.*;

import static org.junit.Assert.*;

public class ScorerTest {

    private static PrimitiveDataset input = new PrimitiveDataset();
    private static LinkedHashMap<String, Object> params = new LinkedHashMap<>();
    private static PrimitiveDataset output;

    @BeforeClass
    public static void score() {
        // get model and testing data
        String modelPath = "src/main/resources/adult_census_pipeline.zip";

        int columnId = 0;
        input.addColumnMetadata(columnId, "age", java.sql.Types.INTEGER, 0, 0);
        input.addIntColumn(columnId, new int[]{39, 50, 38}, null);

        columnId++;
        input.addColumnMetadata(columnId, "hours_per_week", java.sql.Types.INTEGER, 0, 0);
        input.addIntColumn(columnId, new int[]{40, 13, 40}, null);

        columnId++;
        input.addColumnMetadata(columnId, "education", Types.NVARCHAR, 0, 0);
        input.addStringColumn(columnId, new String[]{"Bachelors", "Bachelors", "HS-grad"});

        columnId++;
        input.addColumnMetadata(columnId, "sex", Types.NVARCHAR, 0, 0);
        input.addStringColumn(columnId, new String[]{"Male", "Male", "Male"});

        columnId++;
        input.addColumnMetadata(columnId, "income", Types.NVARCHAR, 0, 0);
        input.addStringColumn(columnId, new String[]{"<=50K", "<=50K", "<=50K"});

        // specify some params
        params.put("logLevel", "INFO"); //default WARN
        params.put("modelPath", modelPath);
        params.put("outputFields", "prediction,probability,education,sex,income,predictedIncome");
        //params.put("outputFields", "features,education-encoded"); //SparseTensor

        // perform scoring
        Scorer scorer = new Scorer();
        scorer.init("session0", 0, 1);
        output = scorer.execute(input, params);

        // cleanup
        scorer.cleanup();
    }

    @Test
    public void outputColumnCountShouldMatch() {
        // display output
        int nOutputCols = output.getColumnCount();
        int nOutputFields = params.getOrDefault("outputFields", "").toString().split(",").length;
        assertEquals(nOutputFields + 1, nOutputCols); // "probability" is a vector field of size 2 in this case
    }

    @Test
    public void outputColumnNamesShouldMatch() {
        int nOutputCols = output.getColumnCount();

        Set<String> columnNames = new HashSet<>();
        for (int iCol = 0; iCol < nOutputCols; iCol++) {
            columnNames.add(output.getColumnName(iCol));
        }
        Set<String> fieldNames = new HashSet<>(Arrays.asList("prediction","probability0","probability1","education","sex","income","predictedIncome"));
        assertEquals(fieldNames, columnNames);
    }

    @Test
    public void outputColumnValuesShouldMatch() {
        String columnName = "education";

        int outputIndex = output.getColumnIndex(columnName);
        String[] outputStringColumn = output.getStringColumn(outputIndex);

        int inputIndex = input.getColumnIndex(columnName);
        String[] inputStringColumn = input.getStringColumn(inputIndex);

        assertArrayEquals(inputStringColumn, outputStringColumn);
    }

    @Test
    public void outputRowCountShouldMatch() {
        int rowCount0 = input.getRowCount(0);
        int[] rowCounts = output.getRowCounts();

        for (int rowCount: rowCounts) {
            assertEquals(rowCount, rowCount0);
        }
    }
}
