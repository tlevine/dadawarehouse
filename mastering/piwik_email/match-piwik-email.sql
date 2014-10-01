-- Dates when visitors visited
CREATE VIEW "ft_piwikvisitor_days" AS
SELECT DISTINCT
  date("serverDateTime") AS "date",
  "visitorId" AS "piwik_id"
FROM ft_piwikvisit;

CREATE TABLE "ft_emailaddress_days" AS
SELECT DISTINCT
  date("datetime") AS "date",
  "from_address" AS "email_address"
FROM ft_notmuchmessage;
