/****** Script for SelectTopNRows command from SSMS  ******/
USE AirLinesDBNew62
GO
/* Авиакомпании  */
SELECT AirLineName AS AIRLINE,
       AirLineAlias AS ALIAS,
	   AirLineCodeIATA AS IATA,
	   AirLineCodeICAO AS ICAO,
	   AirLineCallSighn AS CALLSIGN,
	   AirLineCity AS CITY,
	   AirLineCountry AS COUNTRY,
	   AirLineDescription,
	   AlianceName AS ALIANCE,
	   AirLine_ID
  FROM dbo.AirLinesViewOLD
  WHERE AirLineCodeIATA = '7B' OR AirLineCodeICAO = 'MOA'
  ORDER BY AIRLINE, ALIAS
  -- Почистить ячейки, убрать дубликаты 
  GO