from scripts import DirectoryParser

if __name__ == "__main__":
    model_path_container = 'model_container.pth'
    model_path_trash = 'model_trash.pth'
    source_path = 'image_source'
    service_ip = 'localhost:3000'
    dp = DirectoryParser(source_path, 
                         model_path_container,
                         model_path_trash,
                         service_ip)
    dp.start()