/****** Скрипт для команды SelectTopNRows из среды SSMS  ******/
USE AirFlightsDBNew62Test2
GO

SELECT * 
  FROM dbo.AirCraftsTable
  WHERE AirCraftRegistration IS NULL
		OR AirCraftRegistration = 'Unknown'
		OR AirCraftRegistration = 'UNKNOWN'
		OR AirCraftRegistration = 'nan'
		OR AirCraftRegistration = 'Nan'
		OR AirCraftRegistration = 'NAN'
		OR AirCraftRegistration = 'UNKNOW'
  ORDER BY AirCraftRegistration
GO

SELECT * 
  FROM dbo.AirCraftsViewFull
  WHERE Registration IS NULL
  ORDER BY Model, Manufacturer  --, LN, MSN, SN, CN
GO