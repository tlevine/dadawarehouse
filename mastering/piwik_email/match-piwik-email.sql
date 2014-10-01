-- Dates when visitors visited
CREATE VIEW "ft_piwikvisitor_days" AS
SELECT DISTINCT
  date("serverDateTime") AS "date",
  "visitorId" AS "piwik_id"
FROM ft_piwikvisit;

-- Dates when emailers emailed
CREATE VIEW "ft_emailaddress_days" AS
SELECT DISTINCT
  date("datetime") AS "date",
  "from_address" AS "email_address"
FROM ft_notmuchmessage;

-- Returning visitors
CREATE VIEW "helper_returning_visitors" AS
SELECT "piwik_visitorid"
FROM "ft_piwikvisitor_days"
GROUP BY "piwik_visitorid"
WHERE count(*) >= 2;

-- Returning emailers
CREATE VIEW "helper_returning_emailers" AS
SELECT "email_address"
FROM "ft_emailaddress_days"
GROUP BY "email_address"
WHERE count(*) >= 2;
