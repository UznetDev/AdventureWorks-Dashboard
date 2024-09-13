package com.microsoft.sqlserver.mleap;

import java.sql.JDBCType;
import java.sql.Types;
import java.util.Arrays;

public class PrimitiveDataset extends com.microsoft.sqlserver.javalangextension.PrimitiveDataset {
    public String[] getColumnNames() {
        int nCols = getColumnCount();
        String[] columnNames = new String[nCols];

        for (int iCol = 0; iCol < nCols; iCol++) {
            columnNames[iCol] = getColumnName(iCol);
        }

        return columnNames;
    }

    public int[] getColumnTypes() {
        int nCols = getColumnCount();
        int[] columnTypes = new int[nCols];

        for (int iCol = 0; iCol < nCols; iCol++) {
            columnTypes[iCol] = getColumnType(iCol);
        }

        return columnTypes;
    }

    public int getColumnIndex(String columnName) {
        String[] columnNames = getColumnNames();
        int index = Arrays.asList(columnNames).indexOf(columnName);
        return index;
    }

    public int getRowCount(int iCol) {
        int sqlType = getColumnType(iCol);
        int columnLength;

        switch(sqlType) {
            case Types.BIT:
                columnLength = getBooleanColumn(iCol).length;
                break;
            case Types.SMALLINT:
                columnLength = getShortColumn(iCol).length;
                break;
            case Types.INTEGER:
                columnLength = getIntColumn(iCol).length;
                break;
            case Types.BIGINT:
                columnLength = getLongColumn(iCol).length;
                break;
            case Types.FLOAT:
                columnLength = getFloatColumn(iCol).length;
                break;
            case Types.DOUBLE:
                columnLength = getDoubleColumn(iCol).length;
                break;
            case Types.NVARCHAR:
                columnLength = getStringColumn(iCol).length;
                break;
            case Types.VARBINARY:
                columnLength = getBinaryColumn(iCol).length;
                break;
            case Types.DATE:
                columnLength = getDateColumn(iCol).length;
                break;
            default:
                throw new IllegalArgumentException("unsupported sql type: " + JDBCType.valueOf(sqlType).getName());
        }

        return columnLength;
    }

    public int[] getRowCounts() {
        int nCols = getColumnCount();
        int[] rowCounts = new int[nCols];

        for (int iCol = 0; iCol < nCols; iCol++) {
            rowCounts[iCol] = getRowCount(iCol);
        }

        return rowCounts;
    }
}
