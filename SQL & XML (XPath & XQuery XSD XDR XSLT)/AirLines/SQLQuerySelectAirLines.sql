USE AirLinesDBNew62
GO

SELECT * 
  FROM dbo.AirLinesView
  -- WHERE AlianceName = 'U-FLY Alliance'
  ORDER BY AirLineCodeIATA, AirLineCodeICAO  -- 254

GO