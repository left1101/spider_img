from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def get_index():
   return render_template("index.html")

@app.route('/transform/img', methods=['POST'])
def transform():
    print(request)
    cookie = request.form['inputCookie']
    referer = request.form['inputReferer']
    url = request.form['inputLink']
    imgs= get_content(url, cookie, referer)
    # return jsonify({"code":1,"data":{"list":["//cbu01.alicdn.com/cms/upload/2016/790/696/2696097_1254399316.png","https://cbu01.alicdn.com/img/ibank/2017/698/258/4130852896_248682925.jpg","https://cbu01.alicdn.com/img/ibank/2017/698/258/4130852896_248682925.jpg","https://cbu01.alicdn.com/img/ibank/2017/605/080/4135080506_248682925.jpg","https://cbu01.alicdn.com/img/ibank/2017/271/980/4135089172_248682925.jpg","https://cbu01.alicdn.com/img/ibank/2017/852/078/4130870258_248682925.jpg","https://cbu01.alicdn.com/img/ibank/2017/068/558/4130855860_248682925.jpg"]},"msg":"success"})
    return jsonify({
        "data": {
            "list": imgs,
        },
        "msg": "success",
        "code": 1,
    })

def get_data(url, cookie, referer):
    try:
        headers = {
          'cookie': cookie,
          'referer': referer,
          # 'cookie': '_uab_collina=159385089126308878803496; lid=xiexirru; cna=3PPwFkU1SnECAXMhXHOfYgu7; UM_distinctid=1710b4c9430a52-039bb1ae4077da-396a7f06-384000-1710b4c9431901; CNZZDATA1253659577=1812322654-1593822605-%7C1593822605; taklid=d7dd5655b5e147749e5be677d0aebe51; cookie2=16da148dac5b40bc4517e90692f6939b; t=c5b78b954b5d418d064a36ac9c4e5432; _tb_token_=eb31a7188eebe; __cn_logon__=true; __cn_logon_id__=xiexirru; ali_apache_track=c_mid=b2b-1665824647|c_lid=xiexirru|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; last_mid=b2b-1665824647; cookie1=VWt%2BBbWgCzTlZLEG2rkrfYx1hNSIdx9XMhoG%2BNikTB8%3D; cookie17=UoeyC7bxGSwNHg%3D%3D; sg=u77; csg=3488f929; unb=1665824647; uc4=nk4=0%40GToS3fsSDK7BhZagmLTlDWYJOw%3D%3D&id4=0%40UO%2B0wAXLPpBSUj9BeDYbn7UFIgX1; _nk_=xiexirru; _csrf_token=1593849422786; CNZZDATA1261052687=1524892370-1585032155-%7C1593849697; JSESSIONID=D61525D5C663D7AA370F367E41373A52; x5sec=7b226c61707574613b32223a2238373765313063306333366139313833663836333234623836313837353935644349723467506746454f7a4872626231353775544b786f4d4d5459324e5467794e4459304e7a7378227d; isg=BAwM2auvv19eyKpaulhpm2T_3Ww-RbDva8fa2mbN67da8a_7j1arf9hAkflJuehH; l=eBSnB_iuQwUJxx2dBO5Zlurza779XIRf1sPzaNbMiInca6gA9FMYhNQqM2BpWdtjgt5vMeKP21uf_ReJS2ULSK6QttzXp-m03b96Je1..',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
          # 'referer': 'https://detail.1688.com/pic/546378174082.html/_____tmd_____/verify/?nc_token=0061b516f59fe5bf2373f388d295a386&nc_session_id=01LT_stiRho-10F5345w9zfZs4Ho8sibEv2ZxFwx2MqkfnBDgU6j7Onr_l3m2fkgZ3sUd09YpEZO7DyUmESIdsY_nSmcM57ntI6sK9UWKgGsD_zrBXXoF4dUkeqMweu8uj-sLAJKFB5UZI0rGQnTN_QQ&nc_sig=05oBQ8VZ92FA7wtZq52Mcmp08Z5CqFYxubuObPsX46-hTlp9IsEKM8Fv66Bectz1xxM6v1D11DaxVBwK1VW5Oas_pD5KbchQcLiuIi963F8z75lc5Afznco03uvFreZq-HmJVhNOKpVz143PDFlp06IcDIphKJRZrTMhH5j9GZl1izS5DGHmkZOx84l3GRPQ8GnhT32tsIx7Cnl3b2ig0G3Iuqmz0jyL9LBsh_bhcnwyKUX8FgvruQCz1UfYm4eGPHGD30bYLV_xa19QRRKxMI0csBzUMsK165EDT6F8n9dypRvCuk5UUwHkYjAosVxpiFOpmE90SHtOphjqY4ObSGJ9L7pczPJG8VwucwwIFSVtTH6J2SkdOJep04ZDatOqZSpmQvOFg1n_tYHxBng4JfqQ&x5secdata=5e0c8e1365474455070961b803bd560607b52cabf5960afff39b64ce58073f78c104160ba50db7188fbbe5d92bcc6216ced5c66bde16a66c58da5d5f446324324e885e2fd0db8a9a59e4a1beef82afbbc36a5abfa18c4cf7f2a56d0498392f4d1f7b11ffd5c77bcdd76cfb4200c2b549d7a69f689e1e3ba5f7c0f3bfdf92e461f5ea29d12ebd2a3463f1045db653d43e57066367452c95e78f2a4acf270646a48ea05c33778ef3d87bda466eb6d942355b451f036ca86c1f8b94bad9bae62a8e430858f27485b2a0d804d533640e267324ec97a96e1d92247c2e357256bfb0c8184ef8024e27def8cce485cb401ee26f39ad2fb3f254eab4d35a4a2ce477a28fb068bbeed591d32450270c8f8405c84cc5762a95fc9f16a859fce3419091f9f55708ca06088772a2e2250a8fbb9feead8aa40cf4e8ecfb2e04a2efad864e659941c38f3421d53df4d594e5903daae19a20bc2079d80bb9f79e6f69c7c441da1cd14ae210d0129c5d15ae7e47be3cb781170897eb209e70f360901d4db13ccbb3f5b22bac8505538b7d10979bb77ed9c971bea604728cb48d065d0c18c3d0f9c35903a6085cc09a8ede2e61f3049e99d6dbfbf970dc67662d0515b36b81a67a8b37d14134f757fa850c736adb20f708e6fc54189afd621d85807db309c5440b156b4a8feed984055abd9dd2e5f2355a4a5d9a678964b11679bf2531504047e854&x5step=100&nc_app_key=X82Y__f74a03b354095849f07786e49b5c722a',
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        response = r.text
        # print('response')
        # print(response)
        return response
    except:
        return 'error'

def get_content(url, cookie, referer):
    comments = []

    html = get_data(url, cookie, referer)
    soup = BeautifulSoup(html, 'lxml')

    # f = open('./test.txt','a')
    # f.write(url)
    # f.write('\n')

    # title = soup.find('title')
    # f.write(title.text.strip())
    # f.write('\n')

    img_tags = soup.find_all('img')
    for section in img_tags:
        src = section['src'].replace('.64x64', '')
        comments.append(src)

    return comments


if __name__ == '__main__':
   app.run()
