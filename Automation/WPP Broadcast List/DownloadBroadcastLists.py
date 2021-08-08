from BeautifulSoup import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

# <div class="_2aBzC" style="z-index: 9; transition: none 0s ease 0s; height: 72px; transform: translateY(648px);"><div tabindex="-1" class=""><div data-testid="cell-frame-container" class="_2Z4DV _25uA8"><div class="_2GAT7"><div class="-y4n1" style="height: 49px; width: 49px;"><div class="_27MZN"><span data-testid="default-user" data-icon="default-user" class=""><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 212 212" width="212" height="212"><path fill="#DFE5E7" class="background" d="M106.251.5C164.653.5 212 47.846 212 106.25S164.653 212 106.25 212C47.846 212 .5 164.654.5 106.25S47.846.5 106.251.5z"></path><path fill="#FFF" class="primary" d="M173.561 171.615a62.767 62.767 0 0 0-2.065-2.955 67.7 67.7 0 0 0-2.608-3.299 70.112 70.112 0 0 0-3.184-3.527 71.097 71.097 0 0 0-5.924-5.47 72.458 72.458 0 0 0-10.204-7.026 75.2 75.2 0 0 0-5.98-3.055c-.062-.028-.118-.059-.18-.087-9.792-4.44-22.106-7.529-37.416-7.529s-27.624 3.089-37.416 7.529c-.338.153-.653.318-.985.474a75.37 75.37 0 0 0-6.229 3.298 72.589 72.589 0 0 0-9.15 6.395 71.243 71.243 0 0 0-5.924 5.47 70.064 70.064 0 0 0-3.184 3.527 67.142 67.142 0 0 0-2.609 3.299 63.292 63.292 0 0 0-2.065 2.955 56.33 56.33 0 0 0-1.447 2.324c-.033.056-.073.119-.104.174a47.92 47.92 0 0 0-1.07 1.926c-.559 1.068-.818 1.678-.818 1.678v.398c18.285 17.927 43.322 28.985 70.945 28.985 27.678 0 52.761-11.103 71.055-29.095v-.289s-.619-1.45-1.992-3.778a58.346 58.346 0 0 0-1.446-2.322zM106.002 125.5c2.645 0 5.212-.253 7.68-.737a38.272 38.272 0 0 0 3.624-.896 37.124 37.124 0 0 0 5.12-1.958 36.307 36.307 0 0 0 6.15-3.67 35.923 35.923 0 0 0 9.489-10.48 36.558 36.558 0 0 0 2.422-4.84 37.051 37.051 0 0 0 1.716-5.25c.299-1.208.542-2.443.725-3.701.275-1.887.417-3.827.417-5.811s-.142-3.925-.417-5.811a38.734 38.734 0 0 0-1.215-5.494 36.68 36.68 0 0 0-3.648-8.298 35.923 35.923 0 0 0-9.489-10.48 36.347 36.347 0 0 0-6.15-3.67 37.124 37.124 0 0 0-5.12-1.958 37.67 37.67 0 0 0-3.624-.896 39.875 39.875 0 0 0-7.68-.737c-21.162 0-37.345 16.183-37.345 37.345 0 21.159 16.183 37.342 37.345 37.342z"></path></svg></span></div><img src="https://web.whatsapp.com/pp?e=https%3A%2F%2Fpps.whatsapp.net%2Fv%2Ft61.24694-24%2F95780845_1115500355469573_2599272727985704674_n.jpg%3Fccb%3D11-4%26oh%3D8eeae0896280b9cab50601dcb5c66707%26oe%3D60AFDE10&amp;t=s&amp;u=59898842479%40c.us&amp;i=1588362607&amp;n=UZKh9zNuBZrwO8udcupYy3p0wLsvsJct8VSQnlmIbGY%3D" alt="" draggable="false" class="_18-9u _1bvi5 _3-8er" style="visibility: visible;"></div></div><div class="TbtXF"><div role="gridcell" aria-colindex="2" class="_2pkLM"><div class="_3Dr46"><span class="N2dUK"><span dir="auto" title="Tien Tien" class="_35k-1 _1adfa _3-8er">Tien Tien</span><div class="IGI1I"></div></span></div></div><div class="_1SjZ2"><div class="_2vfYK"><span dir="auto" title="💤" class="_3-8er selectable-text copyable-text"><img crossorigin="anonymous" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="💤" draggable="false" class="b68 emoji apple _3-8er selectable-text copyable-text" data-plain-text="💤" style="background-position: 0px -20px;"></span></div><div role="gridcell" aria-colindex="1" class="_15smv"><span></span><span></span></div></div></div></div></div></div>
chromedriver_path = 'C:\\\\Users\\ignia\\Documents\\Projectos\\Automation\\ChromeDriver\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver_path)
driver.get('https://web.whatsapp.com')

# Código HTML
content = driver.page_source
soup = BeautifulSoup(content)

ChromeOptions = webdriver.chrome.options.Options()
options.setBinary("C:\\Users\\raheela.aslam\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe");  //Path where the Chrome.exe exist in your machine.
System.setProperty("webdriver.chrome.driver", "C:\\chrome_driver\\chromedriver.exe"); 
driver = new ChromeDriver(options);



options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Program Files\Google\Chrome\Application\chrome.exe")
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
driver.get('https://web.whatsapp.com')