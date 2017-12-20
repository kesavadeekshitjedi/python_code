#
# Cookbook:: Apache
# Recipe:: server
#
# Copyright:: 2017, The Authors, All Rights Reserved.

# install the httpd package
package 'httpd' do
        action :install
end

# start the httpd service 
service 'httpd' do
        action [:enable, :start]
end

# create the default index.html file to save in the apache folder
file '/var/www/html/index.html' do
        content '<h1>Default content for basic apache installation</h1>'
end

