USE AirFlightsDBNew62Test2
GO

DECLARE @faildate DATE
SET @faildate = '2005-11-01'  -- 

SELECT * 
  FROM dbo.AirFlightsTable
  WHERE BeginDate = @faildate

DELETE FROM dbo.AirFlightsTable WHERE BeginDate = @faildate

SELECT * 
  FROM dbo.AirFlightsTable
  WHERE BeginDate = @faildate
GO
