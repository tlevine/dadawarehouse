SELECT *
FROM ft_facebookduration
JOIN master_facebook
ON master_facebook.local_id = ft_facebookduration.user_id
WHERE pk = 'blah.blah.blah';
