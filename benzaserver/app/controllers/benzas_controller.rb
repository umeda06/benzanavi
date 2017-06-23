require 'redis'
require 'json'

class BenzasController < ApplicationController
  BENZANAMES = ["5WS1", "5WS2", "5WS3", "5WS4"]
  @@redis = Redis.new

  def index
    benzastatus = @@redis.mget(BENZANAMES)
    benzas = BENZANAMES.zip(benzastatus)
    render :text => Hash[benzas].to_json 
  end
end
