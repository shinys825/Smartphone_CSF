# Library 로딩
library(KoNLP)
library(tm)
library(wordcloud)
library(stringr)
library(readr)
library(foreach)
library(doParallel)

#Sys.setlocale("LC_ALL", "en_US.UTF-8")
#Sys.setenv(LANG = "en_US.UTF-8")
#Sys.setlocale("LC_ALL","English")
#options(encoding = 'UTF-8') 

cl <- makeCluster(4)
registerDoParallel(cl)

useNIADic()

setwd("d:/works/project/phone_csf")
  
ko_tokenizer = function(x) {
  sentence = as.character(x)
  sentence = gsub('[-,~?!.]', ' ', sentence)
  pos = paste(MorphAnalyzer(sentence))
  
  ## 품사별 추출
  extracted = str_match(pos, '([ㄱ-ㅎ가-힣A-z0-9]+)/(f|ncn|ncpa|ncps|paa)')
  len.analyzer = length(extracted[,1])
  
  ## 추출 키워드 통합
  if (len.analyzer == 0) {
      keyword = "none"
      return(keyword)
  }
    else {
        keyword = c(extracted[1:len.analyzer,2])
        keyword = keyword[!is.na(keyword)]
        keyword = paste(keyword, collapse = " ")
        keyword = gsub('[:^:]', '', keyword)
        return(keyword)
    }
}

tokenize = function(df) {
  filtered_df = list()
  count = 0
  for (i in seq(df)) {
    filtered = iconv(ko_tokenizer(df[i]), "UTF-8", localeToCharset()[1])
    filtered_df = append(filtered, filtered_df)
    count = count + 1
    cat('Tokenizer is working... ', count, (count/length(df))*100, '% completed', '\n')
  }
  return(filtered_df)
}

paral_tokenize = function(df) {
    filtered_df = foreach(i = 1:length(df),
                          .combine = rbind,
                          .errorhandling='pass',
                          .packages = c('KoNLP', 'stringr'),
                          .export = 'ko_tokenizer') %dopar% {
        filtered = ko_tokenizer(df[i])
    }
}

raw_data = read_csv('D:/works/project/phone_csf/dataframes/phone_df.csv')

s7_raw = subset(raw_data, select=c("title", "content"), product=="s7")
s7_content = paste(s7_raw$title, s7_raw$content)

s7_ilbe = read_csv('D:/works/project/phone_csf/dataframes/ilbe_s7.csv')
s7_ilbe_content = paste(s7_ilbe$title, s7_ilbe$content)
s7_df = c(s7_content, s7_ilbe_content)

df = paral_tokenize(s7_df)

write.csv(df, file="pcsf_s7_dataframe.csv", row.names = F, col.names = F)

cps = Corpus(VectorSource(df))
tdm = TermDocumentMatrix(cps, control=list(#removeNumbers = T,
                                           #removePunctuation = T,
                                           #tolower=T,
                                           wordLengths=c(4,10),
                                           weighting = weightTf))

#키워드 필터링 및 정리
findFreqTerms(tdm, lowfreq = 5)

## 추출단어 빈도값 설정
len.freq = length(findFreqTerms(tdm, lowfreq = 5))

## 정리 및 추출정리
tdm.matrix = as.matrix(tdm)
word.count = rowSums(tdm.matrix)
word.order = order(word.count, decreasing=T)
rownames(tdm.matrix)[word.order[1:len.freq]]
freq.names = rownames(tdm.matrix)[word.order]

## Weighted Edge 기준 = 설정된 추출단어 빈도값(len.freq)
freq.words = tdm.matrix[word.order[1:len.freq],]

## 비교행렬표 추출
cooccur = freq.words %*% t(freq.words)


# 키워드 빈도 수 파일 저장
write.csv(word.count, 's7_freq.csv', fileEncoding='UTF-8')
write.csv(cooccur, 's7_cooccur.csv')

# 시각화
## WordCloud
### Windows 기본폰트 설정
windowsFonts(nanum = windowsFont("서울남산체 EB"))

### 컬러셋 설정
pal = brewer.pal(6,"Dark2")
pal = pal[-4]

### 빈도수 파일 읽기
word.cloud = read.csv('s7_freq.csv', header = T, stringsAsFactors = F)

wordcloud(word.cloud[,1], word.cloud[,2], min.freq = 3, random.order = F,
          colors = pal, family = "nanum",
          rot.per = 0.1, scale=c(4,0.3), max.words=300)