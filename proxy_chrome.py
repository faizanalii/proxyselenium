from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from dotenv import load_dotenv
import os
load_dotenv()
#Proxy Credentials
PROXY_HOST=os.getenv("PROXY_HOST")
PROXY_PORT=os.getenv("PROXY_PORT")
PROXY_USER=os.getenv("PROXY_USER")
PROXY_PASS=os.getenv("PROXY_PASS")
#Extension
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
#File Name
pluginfile = 'proxy_auth_plugin.zip'
#Zip File
with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_extension(pluginfile)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chromeOptions)
driver.get("https://www.google.com/")