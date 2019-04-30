#!/usr/bin/env python

"""
Script to submit protein dimer to Haddock refinement online
Please change login definitions to your own.
The download is not being perform, rather, the results are available through the email address.
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os
import time

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "GPCRs"


def access_haddock(input_pdb, input_web, user, password):

    """
    Fill Haddock form to submit structure
    """
    query_name = input_pdb[0:-4].upper()
    target_path = home + "/" + input_pdb
    prefs = {"download.default_directory" : download_path}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    #prefs = {"download.default_directory" : download_path}
    driver = webdriver.Chrome(options=options)
    driver.get(input_web)
    driver.find_element_by_name("runname").send_keys(query_name)
    driver.find_element_by_id("foldmenu-p1-title").click()
    drop_1_path = "//select[@name='p1-pdb-mode']/option[@value='submit']"
    driver.find_element_by_xpath(drop_1_path).click()
    chain_1_path = "//select[@name='p1-pdb-chain']/option[@value='A']"
    driver.find_element_by_xpath(chain_1_path).click()
    driver.find_element_by_name("p1-pdb-pdbfile").send_keys(target_path)
    drop_2_path = "//select[@name='p2-pdb-mode']/option[@value='submit']"
    driver.find_element_by_xpath(drop_2_path).click()
    chain_2_path = "//select[@name='p2-pdb-chain']/option[@value='B']"
    driver.find_element_by_xpath(chain_2_path).click()
    driver.find_element_by_name("p2-pdb-pdbfile").send_keys(target_path)
    driver.find_element_by_name("username").send_keys(user)
    driver.find_element_by_name("password").send_keys(password)
    submit_path = "//input[@type='submit']"
    driver.find_element_by_xpath(submit_path).click()

"""
Initialize variables
"""

haddock_web = "https://haddock.science.uu.nl/services/HADDOCK/haddockserver-refinement.html"
download_path = "C:/Users/marti/OneDrive/Desktop/GPCRs"
username = "uc2012154190"
password = "uc2012154190"
home = os.getcwd()

for files in os.listdir(home):
    if files.endswith(".pdb"):
        access_haddock(files, haddock_web, username, password)