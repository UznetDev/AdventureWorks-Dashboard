USE [taxidata]
GO


CREATE FUNCTION [dbo].[fnEngineerFeatures] (
@passenger_count int = 0,
@trip_distance float = 0,
@trip_time_in_secs int = 0,
@direct_distance float = 0)
RETURNS TABLE
AS
  RETURN
  (

	  SELECT
		@passenger_count AS passenger_count,
		@trip_distance AS trip_distance,
		@trip_time_in_secs AS trip_time_in_secs,
		@direct_distance as direct_distance
  )

GO


