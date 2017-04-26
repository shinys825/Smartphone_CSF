# Library 로딩
library(KoNLP)      # 한국어 품사태깅
library(stringr)    # R 정규표현식
library(readr)      # DataFrame reader
library(foreach)    # 병렬처리 반복문
library(doParallel) # 멀티코어 병렬처리 지원

#cl <- makeCluster(4)    # 멀티코어 개수 지정
#registerDoParallel(cl)  # 병렬처리에 등록
useNIADic() # NIADic 사용

setwd("d:/works/project/phone_csf") # 작업경로 지정

# 단어 POS 태깅용 함수
ko_tokenizer = function(x) {
    sentence = as.character(x)
    sentence = gsub('[-,~?!.&;]', ' ', sentence)
    pos = paste(MorphAnalyzer(sentence))
    
    ## 품사별 추출
    extracted = str_match(pos, '([ㄱ-ㅎ가-힣A-z0-9]+)/(paa|ncps|pvg)')
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
}    # 일반단어 추출용

ko_tokenizer2 = function(x) {
  sentence = as.character(x)
  sentence = gsub('[-,~?!.&;]', ' ', sentence)
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
}    # 일반단어 추출용
senti_tokenizer = function(x) {
  sentence = as.character(x)
  sentence = gsub('[-,~?!.&;]', ' ', sentence)
  pos = paste(MorphAnalyzer(sentence))
  
  ## 품사별 추출
  extracted = str_match(pos, '([가-힣]+)/(ncpa|ncps|paa|pvg|nqq)')
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
        return(keyword)
    }
} # 감정단어 추출용

# 문서 처리용 함수
kotok = function(df) {
  filtered_df = list()
  count = 0
  for (i in seq(df)) {
    filtered = ko_tokenizer(df[i])
    filtered_df = append(filtered, filtered_df)
    count = count + 1
    cat('Tokenizer is working... ', count, (count/length(df))*100, '% completed', '\n')
  }
  return(filtered_df)
}  # 문서 일반단어 추출
sentok = function(df) {
    filtered_df = list()
    count = 0
    for (i in seq(df)) {
        filtered = senti_tokenizer(df[i])
        filtered_df = append(filtered, filtered_df)
        count = count + 1
        cat('Tokenizer is working... ', count, (count/length(df))*100, '% completed', '\n')
    }
    return(filtered_df)
} # 문서 감정단어 추출

# 멀티코어 병렬처리 함수
kotok_parel = function(df) {
    filtered_df = foreach(i = 1:length(df),
                          .combine = rbind,
                          .errorhandling='pass',
                          .packages = c('KoNLP', 'stringr'),
                          .export = 'ko_tokenizer') %dopar% {
                              filtered = ko_tokenizer(df[i])
                          }
    }    # 문서 일반단어 추출(Parel)
sentok_parel = function(df) {
    filtered_df = foreach(i = 1:length(df),
                          .combine = rbind,
                          .errorhandling='pass',
                          .packages = c('KoNLP', 'stringr'),
                          .export = 'senti_tokenizer') %dopar% {
                              filtered = senti_tokenizer(df[i])
                          }
    }   # 문서 감정단어 추출(Parel)

# 문서 Text set 생성
raw_data = read_delim('D:/works/project/phone_csf/dataframes/phone_fullframe.csv', '\t') # DataFrame 로딩
phone_text = subset(raw_data, select=c("title", "content")) # DataFrame 제목, 내용 병합
phone_text = paste(phone_text$title, phone_text$content)

# Tokenizing
ko_df = as.matrix(kotok(phone_text))
senti_df = as.matrix(sentok(phone_text))

# 결과저장
write.csv(ko_df, file="pcsf_fullframe2.csv", row.names = F, col.names = F)
write.csv(senti_df, file="pcsf_sentiframe.csv", row.names = F, col.names = F)


MorphAnalyzer("액정에 흠집")
MorphAnalyzer("다시는 안 쓰고 싶다.")
MorphAnalyzer("좋긴하지만 쓰고 싶지만 비싸서 살 수가 없")
MorphAnalyzer("좋기는 한데 사긴싫다")
