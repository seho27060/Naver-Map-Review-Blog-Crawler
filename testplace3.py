import  multiprocessing
import time

import blogCrawler

urls = ['https://blog.naver.com/todl91/222840532404',
              'https://blog.naver.com/mypana777/222129578694',
              'https://blog.naver.com/jmtelecom11/222852505028',
              'https://blog.naver.com/jaejaho/222821057605',
              'https://blog.naver.com/dkswlgp99/222844358146',
              'https://blog.naver.com/wildrosestom/222078742048',
              'https://blog.naver.com/nini4150/222727060863',
              'http://cafe.naver.com/gtakf/3170',
              'https://blog.naver.com/lsy19940715/222816767488',
              'https://blog.naver.com/1027sh/220084053003',
              'https://blog.naver.com/a90608/222705722253',
              'http://cafe.naver.com/bk1009/937111',
              'https://blog.naver.com/xx3020xx/222748954042',
              'https://blog.naver.com/todl91/222718880590',
              'https://blog.naver.com/woorisogogi23/222722478807',
              'https://blog.naver.com/dkaao2000/222574812518',
              'https://blog.naver.com/imgreen_/222747831450',
              'https://blog.naver.com/jin881129/222691501487',
              'https://blog.naver.com/lions7972/222718600368',
              'https://blog.naver.com/ryvius85/222123692326',
              'https://blog.naver.com/tgus6858/222634155008',
              'https://blog.naver.com/dndk6541/222380936821',
              'https://blog.naver.com/ehdtjs1231/222421853658',
              'https://blog.naver.com/dlarl1010/222282546119',
              'https://blog.naver.com/2shhhhh/222097801612',
              'https://blog.naver.com/kkkssssss/222117145805',
              'https://blog.naver.com/and1004to/222430582452',
              'https://blog.naver.com/free7756/221700136935',
              'https://blog.naver.com/hella1989/221573848165',
              'https://blog.naver.com/herapretty/222057628690',
              'https://blog.naver.com/baltong2/221502905965',
              'https://blog.naver.com/hella1989/221772012349',
              'https://blog.naver.com/yingvely/221503475562',
              'https://blog.naver.com/baekml/222077439349',
              'https://blog.naver.com/d3484b/221491697084',
              'https://blog.naver.com/hyunhwaim/221795172178',
              'https://blog.naver.com/sa0024/221029272554',
              'https://blog.naver.com/cjd69akf22/221127576490',
              'https://blog.naver.com/happy_aaaaa/220787347014',
              'https://blog.naver.com/sssung_mi/220865500097',
              'https://blog.naver.com/oksgreen16/221015394622',
              'https://blog.naver.com/zxcdmsrud2/221795875555',
              'https://blog.naver.com/shsh_4554/220747990059',
              'https://blog.naver.com/jisun5845/220704378850',
              'https://blog.naver.com/thisshang/222152457726',
              'http://cafe.naver.com/ludiasset/2096',
              'https://blog.naver.com/heewon5157/222722668549',
              'https://blog.naver.com/heewon5157/222136023039',
              'https://blog.naver.com/house9967/220783936121',
              'https://blog.naver.com/heewon5157/220949610473',
              'https://blog.naver.com/mpmp0701/221571989489',
              'https://blog.naver.com/kbs8382/221512744457',
              'https://blog.naver.com/zitnvi/221530830826']

def resultAppend(getLst,url):
    getLst.append(blogCrawler.blogCrawler(url))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # manager = multiprocessing.Manager()
    # result = manager.list()
    pool = multiprocessing.Pool(processes=4)
    startTime = time.time()
    result = pool.map(blogCrawler.blogCrawler, urls)
    print(result)
    pool.close()
    pool.join()
    resultTime = time.time() - startTime
    print("실행 시간 : {}, 실행 결과 : {}".format(resultTime, len(result)))
