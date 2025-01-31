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
  WHERE AirLineCodeIATA = 'A4' OR AirLineCodeICAO = 'AZO'
  ORDER BY AIRLINE, ALIAS
  -- Почистить ячейки, убрать дубликаты 
  GO