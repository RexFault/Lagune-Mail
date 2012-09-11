<VirtualHost *:80>

	ServerName yaams.lagune-software.com
	ServerAlias www.yaams.lagune-software.com

	ServerAdmin binary@lagune-software.com

	WSGIScriptAlias / /home/yaams/yaams/yaams_site/yaams_site/wsgi.py
	
	Alias /styles/ /home/yaams/yaams/yaams_site/media/styles/
	Alias /images/ /home/yaams/yaams/yaams_site/media/images/
	Alias /static/admin /home/yaams/yaams/yaams_site/media/admin/
	Alias /robots.txt /home/yaams/yaams/yaams_site/media/robots.txt

	<Directory /home/yaams/yaams/yaams/yaams_site/media/admin/>
		Order allow,deny
		Allow from all
	</Directory>

	<Directory /home/yaams/yaams/yaams/yaams_site/yaams_site>
		Order allow,deny
		Allow from all
	</Directory>

	<Directory /home/yaams/yaams/yaams_site/media/styles>
		Order allow,deny
		Allow from all
	</Directory>
	
	<Directory /home/yaams/yaams/yaams_site/media/images>
		Order allow,deny
		Allow from all
	</Directory>

        LogLevel warn

	LogFormat "%m %f %q %s %U %X" custom_format

        CustomLog /var/log/httpd/yaams.log custom_format


</VirtualHost>
