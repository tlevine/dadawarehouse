import sqlalchemy as s

import warehouse.model as m

class PiwikLogVisit(m.Fact):
    idvisit = m.Column(s.Integer, primary_key = True)
    idsite = m.Column(s.Integer)
    idvisitor = m.Column(s.LargeBinary(8))
    visitor_localtime = m.Column(s.Time)
    visitor_returning = m.Column(s.Boolean)
    visitor_count_visits = m.Column(s.Integer)
    visitor_days_since_last = m.Column(s.Integer)
    visitor_days_since_order = m.Column(s.Integer)
    visitor_days_since_first = m.Column(s.Integer)
    visit_first_action_time = m.Column(s.DateTime)
    visit_last_action_time = m.Column(s.DateTime)
    visit_exit_idaction_url = m.Column(s.Integer, default = 0)
    visit_exit_idaction_name = m.Column(s.Integer)
    visit_entry_idaction_url = m.Column(s.Integer)
    visit_entry_idaction_name = m.Column(s.Integer)
    visit_total_actions = m.Column(s.Integer)
    visit_total_searches = m.Column(s.Integer)
    visit_total_events = m.Column(s.Integer)
    visit_total_time = m.Column(s.Integer)
    visit_goal_converted = m.Column(s.Integer)
    visit_goal_buyer = m.Column(s.Integer)
    referer_type = m.Column(s.Integer, nullable = True)
    referer_name = m.Column(s.VARCHAR(70), nullable = True)
    referer_url = m.Column(s.Text)
    referer_keyword = m.Column(s.VARCHAR(255), nullable = True)
    config_id = m.Column(s.LargeBinary(8))
    config_os = m.Column(s.CHAR(3))
    config_os_version = m.Column(s.VARCHAR(100), nullable = True)
    config_browser_name = m.Column(s.VARCHAR(10))
    config_browser_version = m.Column(s.VARCHAR(20))
    config_device_type = m.Column(s.Integer, nullable = True)
    config_device_brand = m.Column(s.VARCHAR(100), nullable = True)
    config_device_model = m.Column(s.VARCHAR(100), nullable = True)
    config_resolution = m.Column(s.VARCHAR(9))
    config_pdf = m.Column(s.Boolean)
    config_flash = m.Column(s.Boolean)
    config_java = m.Column(s.Boolean)
    config_director = m.Column(s.Boolean)
    config_quicktime = m.Column(s.Boolean)
    config_realplayer = m.Column(s.Boolean)
    config_windowsmedia = m.Column(s.Boolean)
    config_gears = m.Column(s.Boolean)
    config_silverlight = m.Column(s.Boolean)
    config_cookie = m.Column(s.Boolean)
    location_ip = m.Column(s.LargeBinary(16))
    location_browser_lang = m.Column(s.VARCHAR(20))
    location_country = m.Column(s.CHAR(3))
    location_region = m.Column(s.CHAR(2), nullable = True)
    location_city = m.Column(s.VARCHAR(255), nullable = True)
    location_latitude = m.Column(s.Float(10,6), nullable = True)
    location_longitude = m.Column(s.Float(10,6), nullable = True)
    custom_var_k1 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_v1 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_k2 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_v2 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_k3 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_v3 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_k4 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_v4 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_k5 = m.Column(s.VARCHAR(200), nullable = True)
    custom_var_v5 = m.Column(s.VARCHAR(200), nullable = True)
    location_provider = m.Column(s.VARCHAR(100), nullable = True)
#   KEY `index_idsite_config_datetime` (`idsite`,`config_id`,`visit_last_action_time`),
#   KEY `index_idsite_datetime` (`idsite`,`visit_last_action_time`),
#   KEY `index_idsite_idvisitor` (`idsite`,`idvisitor`)

CREATE TABLE `piwik_log_link_visit_action` (
  `idlink_va` int(11) NOT NULL AUTO_INCREMENT,
  `idsite` int(10) unsigned NOT NULL,
  `idvisitor` binary(8) NOT NULL,
  `server_time` datetime NOT NULL,
  `idvisit` int(10) unsigned NOT NULL,
  `idaction_url` int(10) unsigned DEFAULT NULL,
  `idaction_url_ref` int(10) unsigned DEFAULT '0',
  `idaction_name` int(10) unsigned DEFAULT NULL,
  `idaction_name_ref` int(10) unsigned NOT NULL,
  `idaction_event_category` int(10) unsigned DEFAULT NULL,
  `idaction_event_action` int(10) unsigned DEFAULT NULL,
  `time_spent_ref_action` int(10) unsigned NOT NULL,
  `custom_var_k1` varchar(200) DEFAULT NULL,
  `custom_var_v1` varchar(200) DEFAULT NULL,
  `custom_var_k2` varchar(200) DEFAULT NULL,
  `custom_var_v2` varchar(200) DEFAULT NULL,
  `custom_var_k3` varchar(200) DEFAULT NULL,
  `custom_var_v3` varchar(200) DEFAULT NULL,
  `custom_var_k4` varchar(200) DEFAULT NULL,
  `custom_var_v4` varchar(200) DEFAULT NULL,
  `custom_var_k5` varchar(200) DEFAULT NULL,
  `custom_var_v5` varchar(200) DEFAULT NULL,
  `custom_float` float DEFAULT NULL,
  PRIMARY KEY (`idlink_va`),
  KEY `index_idvisit` (`idvisit`),
  KEY `index_idsite_servertime` (`idsite`,`server_time`)
) ENGINE=MyISAM AUTO_INCREMENT=560350 DEFAULT CHARSET=utf8;
