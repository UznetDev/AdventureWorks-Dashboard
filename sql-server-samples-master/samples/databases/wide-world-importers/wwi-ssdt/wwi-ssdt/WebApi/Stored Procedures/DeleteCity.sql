﻿CREATE PROCEDURE [WebApi].[DeleteCity](@CityID int)
WITH EXECUTE AS OWNER
AS BEGIN
	DELETE Application.Cities
	WHERE CityID = @CityID
END