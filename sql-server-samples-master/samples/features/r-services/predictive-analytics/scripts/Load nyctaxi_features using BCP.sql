USE taxidata;
GO


BULK INSERT taxidata.dbo.nyctaxi_features
    FROM 'C:\Implementing Predictive Analytics\nyctaxi_features.bcp'
    WITH (
        DATAFILETYPE = 'native'
    );
GO