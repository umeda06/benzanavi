#!/bin/sh
cd benzaserver

# developer mode
#rails s -b 0.0.0.0

# production mode
rake assets:precompile RAILS_ENV=production
rails s -b 0.0.0.0 -e production
