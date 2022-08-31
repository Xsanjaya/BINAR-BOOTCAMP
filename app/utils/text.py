import pandas as pd, re, time, os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from config import AppConfig

config = AppConfig()

factory = StemmerFactory()
stemmer = factory.create_stemmer()

df_slang = pd.read_csv('data/data_set/new_kamusalay.csv', encoding='latin-1', header=None)
df_slang = df_slang.rename(columns={0: 'original', 1: 'default'})

id_stopword_dict = pd.read_csv('data/data_set/stopwordbahasa.csv', header=None)
id_stopword_dict = id_stopword_dict.rename(columns={0: 'stopword'})
stopwords_new    = pd.DataFrame(['sih','nya', 'iya', 'nih', 'biar', 'tau', 'kayak', 'banget'], columns=['stopword'])
id_stopword_dict = pd.concat([id_stopword_dict,stopwords_new]).reset_index()
id_stopword_dict = pd.DataFrame(id_stopword_dict['stopword'])

def remove_unnecessary_char(text):
   new_text = re.sub(r'pic.twitter.com.[\w]+', '', text) # Remove every pic 
   new_text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',new_text) # Remove every URL
   
   new_text = re.sub('gue','saya',new_text) # Sub gue saya
   new_text = re.sub('\n',' ',new_text) # Remove every '\n'
   
   new_text = re.sub(r'[^\x00-\x7F]+',' ', new_text)
   new_text = re.sub(r':', '', new_text)
   new_text = re.sub(r'‚Ä¶', '', new_text)
   
   to_delete = ['hypertext', 'transfer', 'protocol', 'over', 'secure', 'socket', 'layer', 'dtype', 'tweet', 'name', 'object'
               ,'twitter','com', 'pic', ' ya ']
   
   for word in to_delete:
      new_text = re.sub(word,'', new_text)
      new_text = re.sub(word.upper(),' ',new_text)
   
   retweet_user = [' rt ', ' user ']
   
   for word in retweet_user:
      new_text = re.sub(word,' ',new_text) # Remove every retweet symbol & username
      new_text = re.sub(word.upper(),' ',new_text)
      
   new_text = re.sub('  +', ' ', new_text) # Remove extra spaces
   
   result = {'original' : text, 'result' : new_text}
   return result

def remove_nonaplhanumeric(text):
   new_text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
   result = {'original' : text, 'result' : new_text}
   return result

df_slang_map = dict(zip(df_slang['original'], df_slang['default']))

def normalize_slang(text):
   new_text =  ' '.join([df_slang_map[word] if word in df_slang_map else word for word in text.split(' ')])
   result = {'original' : text, 'result' : new_text}
   return result

def remove_stopword(text):
   new_text = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in text.split(' ')])
   new_text = re.sub('  +', ' ', new_text) # Remove extra spaces
   new_text = new_text.strip()
   result = {'original' : text, 'result' : new_text}
   return result

def stemming(text):
   new_text = stemmer.stem(text)
   
   result = {'original' : text, 'result' : new_text}
   return result

def preprocess(text):
   new_text = text.lower()
   new_text = remove_unnecessary_char(new_text)['result']
   new_text = remove_nonaplhanumeric(new_text)['result']
   new_text = normalize_slang(new_text)['result']
   new_text = stemming(new_text)['result']
   new_text = remove_stopword(new_text)['result']
   result = {'original' : text, 'result' : new_text}
   return result

def csv_text(text):
   return preprocess(text)['result']

def fileremover(dir_path, limitfile=10):
   count = 0
   files = []
   for x in os.listdir(dir_path):
      if os.path.isfile(os.path.join(dir_path, x)):
         files.append(x)
         count += 1
   
   if count>=limitfile:
      for i in range(int(limitfile/2)):
         os.remove(f"{dir_path}{files[i-1]}")


def csv_cleaning(file, col_name, encoding='latin-1', delimiter=','):
   
   df = pd.read_csv(file, encoding=encoding, delimiter=delimiter)
   df.insert(1, f'{col_name}_Result', df[col_name].apply(csv_text))

   now = time.strftime("%H%M%S_%d%m%Y")
   file_name = f"file_response_{now}.csv"
   df.to_csv(f"{config.UPLOAD_FOLDER}{file_name}")
   fileremover(f"{config.UPLOAD_FOLDER}", limitfile=10)
   return file_name