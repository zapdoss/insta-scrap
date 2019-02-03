from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import xlrd

import requests

#scraps 320X320 images(square) from instagram posts of any instagram user. Mainly meant for collecting data to train a prediction model.


driver = webdriver.Chrome('path to chromedriver')


def scrapy(username):
        driver.get("https://www.instagram.com/"+username)

        userinfo = driver.find_elements_by_class_name('g47SY')
        posts = userinfo[0].text
        followers =userinfo[1].get_attribute('title')
        following = userinfo[2].text

        posts=posts.replace(',','')
        followers=followers.replace(',','')
        following=following.replace(',','')

        #print posts, followers, following

        prev = 0;
        for j in range(6):

            driver.execute_script("window.scrollTo("+str(prev) + ", "+str(prev+300) + ");")
            prev=prev+300

            for i in range(1,4):
                
                try:

                    try:
                        post =  '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[' +str(j+1)+ ']/div[' + str(i) +  ']/a'
                        xpath = post + "/div/div[1]/img"
                        element = driver.find_element_by_xpath(xpath)
                    except:
                        post =  '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[' +str(j+1)+ ']/div[' + str(i) +  ']/a'
                        xpath = post + "/div/div[1]/img"
                        element = driver.find_element_by_xpath(xpath)
                    
                    finally:
                        srcset = element.get_attribute("srcset")
                        link = (srcset.split(',')[2]).split(' ')[0]

                        video = 0;
                        try:
                            if(driver.find_element_by_xpath(post+'/div[2]/div/span').get_attribute('aria-label')== "Video"):
                                video = 1
                        except:
                            video = 0

                        element = driver.find_element_by_xpath(post)

                        action=ActionChains(driver).move_to_element(element)
                        action.perform()


                        try:
                            likes = driver.find_element_by_xpath(post + '/div[3]/ul/li[1]/span[1]').text
                        except:
                            likes = driver.find_element_by_xpath(post + '/div[2]/ul/li[1]/span[1]').text

                        likes=likes.replace(',','')

                        #print link, likes
                        r = requests.get(link, allow_redirects=True)
                        imgname = username+"_"+str(3*j+i)
                        open('images/'+str(imgname), 'wb').write(r.content)
                        lst =  [username, posts, followers, following, imgname, likes, video]
                        print lst

                        with open('data.csv','a') as fd:
                            writer = csv.writer(fd)
                            writer.writerow(lst)

                except:
                    continue



#scrapy("danbilzerian")


driver.close()
