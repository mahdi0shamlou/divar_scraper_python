import os
import time
while True:
        print('Restarting Divar scraper')
        os.system("sudo systemctl restart Restart_POST_ROW_service.service")
        os.system("sudo systemctl restart Restart_POST_DETAILS_service.service")
        print('Restarted Divar scraper')
        time.sleep(3000)
