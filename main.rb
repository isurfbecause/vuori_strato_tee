require 'json'

PRODUCT_SIZE = 'm'

def parse_json_file(file_path)
  begin
    data = JSON.parse(File.read(file_path))

    data['hasVariant'].each do |tee|
      if tee.key?('name') && !tee['name'].empty? && tee['offers']['availability'] == "InStock"
        size = tee['size'].downcase!.strip
        price = tee['offers']['price']

        if PRODUCT_SIZE == size
          puts tee
          puts "size:#{size}"
          puts tee['offers']['price']
        end
      end
    end


  rescue Errno::ENOENT => e
    puts "File #{file_path} not found."
  rescue JSON::ParserError => e
    puts "JSON parse error: #{e.message}"
  end
end

# usage
file_path = 'data.json'
parse_json_file(file_path)
