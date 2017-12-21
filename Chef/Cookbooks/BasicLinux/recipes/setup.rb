package 'tree' do
	action :install
end
package 'ntp' do
	action :install
end
service 'ntpd' do
	action [:enable, :start]
end
package 'emacs' do
	action :install
end

file '/etc/motd' do
	content "This server belongs to DK
	HOSTNAME: #{node['hostname']}
	IPADDRESS: #{node['ipaddress']}
	TOTAL MEMORY: #{node['memory']['total']}
	TOTAL SWAP  : #{node['memory']['swap']['total']}
"
	
end
# printing something using a variable
# if we are using variables, then use double quotes around the string.
# a variable is identified using the following way #{variable}
apple_count =4
puts "I have #{apple_count} apples"

file '/var/www/html/index.html' do
	content " Host information is as follows:
	<p>
	HOSTNAME: #{node['hostname']}
        IPADDRESS: #{node['ipaddress']}
        TOTAL MEMORY: #{node['memory']['total']}
        TOTAL SWAP  : #{node['memory']['swap']['total']}
	</p>
"
end
