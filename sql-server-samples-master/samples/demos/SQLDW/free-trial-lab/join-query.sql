-- Join Date table and Trip table

SELECT TOP (1000000) dt.[DayOfWeek]
      ,tr.[MedallionID]
      ,tr.[HackneyLicenseID]
      ,tr.[PickupTimeID]
      ,tr.[DropoffTimeID]
      ,tr.[PickupGeographyID]
      ,tr.[DropoffGeographyID]
      ,tr.[PickupLatitude]
      ,tr.[PickupLongitude]
      ,tr.[PickupLatLong]
      ,tr.[DropoffLatitude]
      ,tr.[DropoffLongitude]
      ,tr.[DropoffLatLong]
      ,tr.[PassengerCount]
      ,tr.[TripDurationSeconds]
      ,tr.[TripDistanceMiles]
      ,tr.[PaymentType]
      ,tr.[FareAmount]
      ,tr.[SurchargeAmount]
      ,tr.[TaxAmount]
      ,tr.[TipAmount]
      ,tr.[TollsAmount]
      ,tr.[TotalAmount]
  FROM [dbo].[Trip] as tr
  join
  dbo.[Date] as dt
  on tr.DateID = dt.DateID
