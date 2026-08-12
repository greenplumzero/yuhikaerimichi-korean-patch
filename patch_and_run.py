from pathlib import Path
import certifi
import ssl
import struct, hashlib, urllib.request, gzip, sys, os, subprocess, webbrowser, time, threading
import lz4.block

PAIRS = [('おしまい', '끝'), ('ほんぶんのてきすと', '본문 텍스트'), ('いっしょにかーえろ！', '같이 가자!'), ('とちゅうまで おなじ道だったよね', '중간까지는 같은 길이었지?'), ('あ、そうだ', '아, 맞다'), ('せっかくなら かえりながら', '모처럼이니까 집에 가면서'), ('『かくれんぼ』しようよ', '『숨바꼭질』 하자'), ('決まりね！', '결정이야!'), ('じゃあ ゆいなが かくれるから', '그럼 유이나가 숨을 테니까'), ('かえりながら さがしてね！', '집에 가면서 찾아줘!'), ('（先に行っちゃった・・・）', '（먼저 가버렸네・・・）'), ('（かくれんぼかぁ）', '（숨바꼭질인가）'), ('（ゆいなちゃん を みつけなきゃ）', '（유이나를 찾아야 해）'), ('（今日こそ ゆいなちゃん を みつけなきゃ）', '（오늘이야말로 유이나를 찾아야 해）'), ('見つかっちゃった！', '찾아버렸네!'), ('じゃあ帰ろ！', '그럼 가자!'), ('今日もかくれんぼしよ！', '오늘도 숨바꼭질하자!'), ('ねぇ、知ってる？', '있잖아, 알아?'), ('先生から きいたんだけど', '선생님한테 들었는데'), ('ひとりで かえってると', '혼자 집에 가고 있으면'), ('ユウレイ が 出るんだって！', '유령이 나온대!'), ('こわいよね・・・', '무섭지・・・'), ('ということで 気を付けてね！', '그러니까 조심해서 가!'), ('じゃあ 今日もよろしく！', '그럼 오늘도 부탁해!'), ('（ゆいなちゃん、なんでそんなこと言うの～）', '（유이나, 왜 그런 말을 하는 거야~）'), ('（こわい話 ニガテなのに・・・）', '（무서운 얘기 싫은데・・・）'), ('（はやく みつけなきゃ）', '（빨리 찾아야 해）'), ('（ユウレイ、いませんように！）', '（유령이 없기를!）'), ('（ゆいなちゃん、どこにいるんだろう）', '（유이나, 어디 있는 걸까）'), ('また見つかっちゃった！', '또 찾아버렸네!'), ('見つけるのうまいね', '찾는 거 진짜 잘한다'), ('じゃまたあした！', '그럼 내일 봐!'), ('みなさんにお話があります', '여러분께 할 말이 있습니다'), ('ここ最近、学校の近くで', '최근 학교 근처에서'), ('フシンシャが もくげきされています', '수상한 사람이 목격되고 있습니다'), ('知らない人をジロジロと見ないように', '모르는 사람을 빤히 보지 말고'), ('気を付けて 帰りましょう', '조심해서 돌아갑시다'), ('じゃあ今日もかくれんぼね！', '그럼 오늘도 숨바꼭질이야!'), ('（フシンシャ・・・）', '(수상한 사람・・・)'), ('（知らない人は みないように・・・）', '(모르는 사람은 보지 말자・・・)'), ('（ゆいなちゃん、だいじょうぶかな）', '（유이나, 괜찮으려나）'), ('（ゆいなちゃん、どこにいるんだろう）', '（유이나, 어디 있는 걸까）'), ('えー！見つけるのじょうず！', '에이~! 찾는 거 너무 잘해!'), ('ねぇ、だいじょうぶだった？', '있잖아, 괜찮았어?'), ('変な人 いたよね？', '이상한 사람 봤지?'), ('ずっとこっち見てたし', '계속 이쪽 보고 있었고'), ('まだ見てる！ はやく かえろ！', '아직도 보고 있어! 빨리 가자!'), ('ねぇ・・・', '있잖아...'), ('『ふわふわさん』 って 知ってる？', '『후와후와 씨』라고 알아?'), ('おかあさん に 聞いたんだけど', '엄마한테 들었는데'), ('このへんの どこかで たまに', '이 근처 어딘가에 가끔'), ('ふわふわ', '둥실둥실'), ('って カゲ が ういてて', '하는 그림자가 떠 있고'), ('じっと 見ちゃうと', '가만히 쳐다보면'), ('つれていかれる', '데려간대'), ('んだって', '그렇대'), ('ふわふわ～って つれていかれちゃうんだって！', '둥실둥실~ 하면서 데려가 버린대!'), ('それが 『ふわふわさん』', '그게 『후와후와 씨』래'), ('こわいよね～', '무섭지~'), ('じゃあ ゆいな、今日は', '그럼 유이나는 오늘'), ('おかあさん が むかえにきてくれてるから', '엄마가 데리러 와 주기로 해서'), ('おかあさん と かえるね！', '엄마랑 같이 갈게!'), ('じゃあ またあした！', '그럼 내일 봐!'), ('（『ふわふわさん』・・・）', '（『후와후와 씨』・・・）'), ('（こわいなぁ・・・）', '（무서워・・・）'), ('（みちゃ いけないんだっけ）', '（보면 안 된다고 했지）'), ('かえろ・・・', '가자・・・'), ('こわいなぁ', '무섭다...'), ('ただいまー', '다녀왔어~'), ('（とちゅうに\u3000いたよね・・・）', '（가는 길에 있었지・・・）'), ('（『ふわふわさん』・・・）', '（『후와후와 씨』・・・）'), ('（いるんだ・・・ホントに・・・）', '（있구나・・・진짜로・・・）'), ('ふわふわさん いたって ホント！？', '후와후와 씨 봤다는 거 진짜야!?'), ('ホントに いるんだ・・・', '진짜로 있구나・・・'), ('じゃあ 今日も かくれんぼね！', '그럼 오늘도 숨바꼭질이야!'), ('ずるい・・・', '치사해・・・'), ('（もしかして・・・）', '（설마・・・）'), ('（ふわふわさんを さがしにいっちゃった？）', '（후와후와 씨를 찾으러 간 거야?）'), ('（だいじょうぶかな？）', '（괜찮으려나?）'), ('（止めにいかなきゃ！）', '（말리러 가야 해!）'), ('（ゆいなちゃん いなかったな）', '（유이나는 없었네）'), ('（先に 帰っちゃったのかな）', '（먼저 집에 간 걸까）'), ('（またあした\u3000かくれんぼ しよう）', '（내일 또 숨바꼭질하자）'), ('みなさんに、悲しいお知らせがあります', '여러분께 슬픈 소식이 있습니다'), ('昨日・・・ ゆいなさん が亡くなりました', '어제・・・ 유이나가 세상을 떠났습니다'), ('先生、もう、どうしたらいいか・・・', '선생님도 이젠 어쩌지・・・'), ('とても、とてもかなしいです', '정말, 정말 슬픕니다'), ('みなさん、気を付けて帰ってください', '여러분, 조심해서 돌아가세요'), ('本当に、気を付けて・・・', '정말로, 조심하세요・・・'), ('（ゆいな ちゃん・・・）', '（유이나・・・）'), ('（ふわふわさん に ）', '（후와후와 씨에게 ）'), ('（つれていかれちゃったのかな？）', '（끌려가 버린 걸까?）'), ('（でも 見ちゃだめって しってたのに ）', '(보면 안 되는 걸 알았는데 )'), ('（なんで・・・？）', '（왜・・・?）'), ('（ふわふわさん って、一体・・・？）', '（후와후와 씨는 대체・・・?）'), ('（なにか ヒントはないかな？）', '（뭔가 단서는 없을까?）'), ('（ふわふわさん って、一体・・・？）', '（후와후와 씨는 대체・・・?）'), ('（なにか ヒントはないかな？）', '（뭔가 단서는 없을까?）'), ('（いろいろ みえた 気がする）', '(여러 가지가 보인 것 같아)'), ('（そういえば 電柱の下の お花・・・）', '（그러고 보니 전봇대 밑의 꽃・・・）'), ('（なんでいつも 置いてあるんだろう）', '（왜 항상 놓여 있는 걸까）'), ('ひとりに なっちゃった', '혼자가 돼 버렸네'), ('コワいときはね', '무서울 땐 있지'), ('見ちゃえばいいんだよ', '그냥 보면 돼'), ('コワくなくなるよ', '안 무서워질 거야'), ('ただいま！', '다녀왔어!'), ('はぁ・・・ちくしょう・・・', '하아・・・젠장・・・'), ('オレの人生なんなんだ・・・', '내 인생은 대체 뭐냐・・・'), ('あ？ 何見てんだよ', '어? 뭘 쳐다봐'), ('ガキが、文句でもあんのか！？', '꼬맹이가, 불만이라도 있냐!?'), ('お前もオレをバカにすんのか？', '너도 날 무시하는 거냐?'), ('さっさと帰りやがれ！', '썩 꺼져!'), ('（こわい！）', '（무서워!）'), ('（今日はもうムリ！）', '(오늘은 무리야!)'), ('（かえる！）', '(집에 갈래!)'), ('（あれ？）', '（어라?）'), ('（ゆいなちゃん どこにいたんだろ？）', '（유이나는 어디에 있었던 거지?）'), ('（先に 帰っちゃったのかな？）', '（먼저 집에 간 걸까?）'), ('おいって！！', '야!!'), ('オレのこと 笑ってたろ', '나 비웃었지'), ('お前もオレをバカにすんのか？', '너도 날 무시하는 거냐?'), ('フワフワ だの フラフラ だの しらねーけど', '후와후와든 뭐든 모르겠지만'), ('聞こえてんだよ', '다 들리거든'), ('オレのことバカにしてんだろ？', '나 무시하는 거잖아?'), ('この前の ガキみてーにさぁ！', '저번 그 꼬맹이처럼 말이야!'), ('オレだって毎日毎日毎日毎日', '나도 매일매일매일매일'), ('グチグチグチグチグチグチグチグチグチ', '잔소리잔소리잔소리잔소리잔소리'), ('バカ共に言われてるけどがまんして', '멍청한 놈들한테 들어도 참고'), ('たえてたえてたえてたえてたえてたえて', '참고참고참고참고참고참고'), ('なのにおまえたちはおれをばかにして', '그런데 너희는 날 무시하고'), ('フワフワ してる バカ だっていいたいのか', '둥실대는 바보라고 하고 싶냐'), ('お前 も 殺してやろうか', '너도 죽여버릴까'), ('お前 も 殺してやる', '너도 죽여버린다'), ('お前も殺すお前も殺すお前も殺す', '너도 죽여 너도 죽여 너도 죽여'), ('殺す殺す殺す殺す殺す殺す殺す', '죽여죽여죽여죽여죽여죽여죽여'), ('にげるな！！！', '도망가지 마!!!'), ('にげなきゃ！！！', '도망쳐야 해!!!'), ('カギ かけやがったか', '문 잠갔냐'), ('クソガキが！', '망할 꼬마!'), ('家 おぼえたからな！', '집 기억해 뒀으니까!')]

DATA_URL='https://os-worker.unityroom.com/unityroom_production/game/67884/webgl/webgl.data.gz?h=1758218824'
LOADER_URL='https://os-worker.unityroom.com/unityroom_production/game/67884/webgl/webgl.loader.js?h=1758218824'
FRAMEWORK_URL='https://os-worker.unityroom.com/unityroom_production/game/67884/webgl/webgl.framework.js.gz?h=1758218824'
WASM_URL='https://os-worker.unityroom.com/unityroom_production/game/67884/webgl/webgl.wasm.gz?h=1758218824'
EXPECTED_WEB_SHA='ce1607f3bdb1d7d4bb8a4b164dfe7d05cc27a3cecd7b520a63fdce5d6662901a'
MAGIC=b'UnityWebData1.0\x00'
PATCH_VERSION='1.4-fast-cache'

def sha256(b): return hashlib.sha256(b).hexdigest()

def read_cstr(buf,pos):
    end=buf.index(0,pos);return bytes(buf[pos:end]).decode('utf-8','replace'),end+1

def parse_bundle(raw):
    p=0; sig,p=read_cstr(raw,p)
    if sig!='UnityFS': raise RuntimeError('UnityFS 아카이브가 아닙니다.')
    version=struct.unpack_from('>I',raw,p)[0];p+=4
    unity_ver,p=read_cstr(raw,p);unity_rev,p=read_cstr(raw,p)
    total_size=struct.unpack_from('>Q',raw,p)[0];p+=8
    cinfo_size,uinfo_size,flags=struct.unpack_from('>III',raw,p);p+=12
    header_end=p
    info_pos=total_size-cinfo_size if flags&0x80 else (((p+15)//16)*16 if flags&0x200 else p)
    cinfo=raw[info_pos:info_pos+cinfo_size]
    ctype=flags&0x3f
    if ctype==0: info=cinfo
    elif ctype in (2,3): info=lz4.block.decompress(cinfo,uncompressed_size=uinfo_size)
    else: raise RuntimeError(f'지원하지 않는 UnityFS 압축 형식: {ctype}')
    q=16; count=struct.unpack_from('>I',info,q)[0];q+=4
    blocks=[]
    for _ in range(count):
        us,cs,fl=struct.unpack_from('>IIH',info,q);q+=10;blocks.append([us,cs,fl])
    dcount=struct.unpack_from('>I',info,q)[0];q+=4;dirs=[]
    for _ in range(dcount):
        off,size,fl=struct.unpack_from('>QQI',info,q);q+=20
        name,q=read_cstr(info,q);dirs.append((off,size,fl,name))
    if flags&0x80: data_pos=((header_end+15)//16)*16 if flags&0x200 else header_end
    else:
        data_pos=info_pos+cinfo_size
        if flags&0x200:data_pos=((data_pos+15)//16)*16
    compressed=[];x=data_pos
    for us,cs,fl in blocks:compressed.append(raw[x:x+cs]);x+=cs
    return dict(version=version,unity_ver=unity_ver,unity_rev=unity_rev,flags=flags,info_hash=info[:16],blocks=blocks,dirs=dirs,compressed=compressed)

def decompress_bundle(raw):
    bun=parse_bundle(raw);out=bytearray()
    for (us,cs,fl),comp in zip(bun['blocks'],bun['compressed']):
        typ=fl&0x3f
        if typ==0:d=comp
        elif typ in (2,3):d=lz4.block.decompress(comp,uncompressed_size=us)
        else:raise RuntimeError(f'지원하지 않는 데이터 압축 형식: {typ}')
        if len(d)!=us:raise RuntimeError('UnityFS 블록 크기가 맞지 않습니다.')
        out+=d
    return bun,bytes(out)

def build_bundle(bun,logical,dirs=None):
    if dirs is None:dirs=bun['dirs']
    block_size=1024*1024;blocks=[];compressed=[]
    for i in range(0,len(logical),block_size):
        ch=bytes(logical[i:i+block_size])
        c=lz4.block.compress(ch,mode='fast',acceleration=1,store_size=False)
        if len(c)>=len(ch):c,fl=ch,0
        else:fl=3
        blocks.append((len(ch),len(c),fl));compressed.append(c)
    info=bytearray(bun['info_hash'])+struct.pack('>I',len(blocks))
    for us,cs,fl in blocks:info+=struct.pack('>IIH',us,cs,fl)
    info+=struct.pack('>I',len(dirs))
    for off,size,fl,name in dirs:info+=struct.pack('>QQI',off,size,fl)+name.encode()+b'\0'
    cinfo=lz4.block.compress(bytes(info),mode='fast',acceleration=1,store_size=False)
    if len(cinfo)<len(info):info_flag=3
    else:cinfo=bytes(info);info_flag=0
    flags=(bun['flags']&~0x3f)|info_flag
    head=bytearray(b'UnityFS\0')+struct.pack('>I',bun['version'])+bun['unity_ver'].encode()+b'\0'+bun['unity_rev'].encode()+b'\0'
    size_pos=len(head);head+=b'\0'*8+struct.pack('>III',len(cinfo),len(info),flags)
    if flags&0x200:head+=b'\0'*((16-len(head)%16)%16)
    body=bytearray(cinfo)
    if flags&0x200:body+=b'\0'*((16-(len(head)+len(body))%16)%16)
    for c in compressed:body+=c
    struct.pack_into('>Q',head,size_pos,len(head)+len(body))
    return bytes(head)+bytes(body)

def parse_webdata(blob):
    if not blob.startswith(MAGIC):raise RuntimeError('webgl.data 형식이 올바르지 않습니다.')
    hlen=struct.unpack_from('<I',blob,16)[0];p=20;ents=[]
    while p<hlen:
        off,size,nl=struct.unpack_from('<III',blob,p);p+=12
        name=blob[p:p+nl].decode();p+=nl;ents.append((name,off,size))
    return ents

def rebuild_webdata(blob,new_bundle):
    ents=parse_webdata(blob);payloads=[]
    for name,off,size in ents:payloads.append((name,new_bundle if name=='data.unity3d' else blob[off:off+size]))
    hlen=20+sum(12+len(n.encode()) for n,_ in payloads);cur=hlen
    hdr=bytearray(MAGIC+struct.pack('<I',hlen))
    for name,data in payloads:
        nb=name.encode();hdr+=struct.pack('<III',cur,len(data),len(nb))+nb;cur+=len(data)
    return bytes(hdr)+b''.join(data for _,data in payloads)

def extract_bundle(web):
    for name,off,size in parse_webdata(web):
        if name=='data.unity3d':return web[off:off+size]
    raise RuntimeError('data.unity3d를 찾지 못했습니다.')

def pad_utf8(text,target_len):
    b=text.encode();
    if len(b)>target_len:raise RuntimeError(f'번역문이 원문보다 깁니다: {text}')
    rem=target_len-len(b)
    return b+(b'\xe2\x80\x8b'*(rem//3))+(b' '*(rem%3))

def patch_initial_dialogue(bundle_raw):
    bun,logical=decompress_bundle(bundle_raw);logical=bytearray(logical)
    target=next(d for d in bun['dirs'] if d[3]=='level2');lo,sz,_,_=target;hi=lo+sz
    reps=sorted(PAIRS,key=lambda x:len(x[0].encode()),reverse=True);found=0
    # patch whole level2, byte-length preserving
    region=bytearray(logical[lo:hi])
    for jp,ko in reps:
        old=jp.encode();rep=pad_utf8(ko,len(old));pos=0
        while True:
            i=region.find(old,pos)
            if i<0:break
            region[i:i+len(old)]=rep;found+=1;pos=i+len(old)
    if found<140:raise RuntimeError(f'대사 패턴을 {found}개만 찾았습니다. 예상 게임 버전과 다릅니다.')
    logical[lo:hi]=region
    return build_bundle(bun,logical)

def parse_serialized_objects(asset):
    ver=struct.unpack_from('>I',asset,8)[0]
    if ver<22:raise RuntimeError('지원하지 않는 SerializedFile 버전')
    endian='>' if asset[16] else '<';data_offset=struct.unpack_from('>Q',asset,32)[0]
    p=48;q=asset.index(0,p);p=q+1;p+=4;enable=asset[p];p+=1
    type_count=struct.unpack_from(endian+'i',asset,p)[0];p+=4;types=[]
    for _ in range(type_count):
        cid=struct.unpack_from(endian+'i',asset,p)[0];p+=4;p+=1;p+=2
        if cid==114:p+=16
        p+=16
        if enable:
            nc,ss=struct.unpack_from(endian+'ii',asset,p);p+=8;p+=nc*(32 if ver>=19 else 24)+ss
            if ver>=21:
                depc=struct.unpack_from(endian+'i',asset,p)[0];p+=4+depc*4
        types.append(cid)
    object_count=struct.unpack_from(endian+'i',asset,p)[0];p+=4;objs=[]
    for _ in range(object_count):
        p=(p+3)&~3;pid=struct.unpack_from(endian+'q',asset,p)[0];p+=8
        start_pos=p;start=struct.unpack_from(endian+'q',asset,p)[0];p+=8
        size_pos=p;size=struct.unpack_from(endian+'I',asset,p)[0];p+=4
        tid=struct.unpack_from(endian+'i',asset,p)[0];p+=4
        objs.append({'pid':pid,'start':start,'size':size,'tid':tid,'cid':types[tid],'start_pos':start_pos,'size_pos':size_pos})
    return data_offset,objs

def patch_font(bundle_raw,ttf):
    bun,logical=decompress_bundle(bundle_raw)
    rdir=next(d for d in bun['dirs'] if d[3]=='resources.assets');roff,rsize,rfl,rname=rdir
    asset=logical[roff:roff+rsize];data_offset,objs=parse_serialized_objects(asset)
    target=next(o for o in objs if o['cid']==128 and o['pid']==165)
    raw=bytearray(asset[data_offset+target['start']:data_offset+target['start']+target['size']])
    sig=2216;old_len=struct.unpack_from('<I',raw,sig-4)[0]
    if raw[sig:sig+4]!=b'\x00\x01\x00\x00':raise RuntimeError('기존 폰트 데이터를 찾지 못했습니다.')
    newraw=raw[:sig-4]+struct.pack('<I',len(ttf))+ttf+raw[sig+old_len:]
    meta=bytearray(asset[:data_offset]);payload=bytearray()
    for o in sorted(objs,key=lambda x:x['start']):
        while len(payload)%8:payload.append(0)
        new_start=len(payload);objraw=newraw if o['pid']==target['pid'] else asset[data_offset+o['start']:data_offset+o['start']+o['size']]
        meta[o['start_pos']:o['start_pos']+8]=struct.pack('<q',new_start)
        meta[o['size_pos']:o['size_pos']+4]=struct.pack('<I',len(objraw));payload+=objraw
    res2=meta+payload;res2[24:32]=struct.pack('>Q',len(res2))
    logical2=logical[:roff]+res2+logical[roff+rsize:]
    dirs=[(off,len(res2) if name=='resources.assets' else size,fl,name) for off,size,fl,name in bun['dirs']]
    return build_bundle(bun,logical2,dirs)

def fixed_replace(buf,old,new,count_exact=None):
    ob=old.encode();nb=new.encode()
    if len(nb)>len(ob):raise RuntimeError(f'고정 길이 치환 불가: {old} -> {new}')
    cnt=buf.count(ob)
    if count_exact is not None and cnt!=count_exact:raise RuntimeError(f'{old!r} 발견 수 {cnt}, 예상 {count_exact}')
    rep=nb+b' '*(len(ob)-len(nb));return bytearray(bytes(buf).replace(ob,rep)),cnt

def replace_serialized_string(buf,old_text,new_text):
    oldb=old_text.encode();newb=new_text.encode();pos=buf.find(oldb)
    if pos<0:raise RuntimeError(f'문자열을 찾지 못했습니다: {old_text}')
    lenpos=pos-4;old_declared=struct.unpack_from('<I',buf,lenpos)[0]
    old_end=pos+old_declared;old_aligned=(old_end+3)&~3
    new_field=struct.pack('<I',len(newb))+newb+b'\0'*((4-len(newb)%4)%4)
    growth=len(new_field)-(old_aligned-lenpos)
    return buf[:lenpos]+new_field+buf[old_aligned:],growth

def rewrite_fixed_serialized_string(buf,old_text,new_text):
    ob=old_text.encode();nb=new_text.encode();pos=buf.find(ob)
    if pos<0:raise RuntimeError(f'문자열을 찾지 못했습니다: {old_text}')
    declared=struct.unpack_from('<I',buf,pos-4)[0]
    if len(nb)>declared:raise RuntimeError(f'문자열 슬롯이 부족합니다: {new_text}')
    buf[pos:pos+declared]=nb+b' '*(declared-len(nb))

def patch_extras(bundle_raw):
    bun,logical=decompress_bundle(bundle_raw);logical=bytearray(logical)
    # Safe/global extras before structural edits
    for old,new,expected in [
        ('おーい','어이!',1),('ゆいな','유이나',2),('かえる','귀가',1),('유령','귀신',2),('チッ','쳇',1)
    ]:
        logical,_=fixed_replace(logical,old,new,expected)

    # level2 object edits
    level_dir=next(d for d in bun['dirs'] if d[3]=='level2');level_off,level_size,_,_=level_dir
    level=bytearray(logical[level_off:level_off+level_size]);data_offset=struct.unpack_from('>Q',level,32)[0]
    entry_start=1760
    def obj_info(pid):
        off=entry_start+(pid-1)*24;path,bs,sz,tid=struct.unpack_from('<qQIi',level,off)
        if path!=pid:raise RuntimeError(f'Path ID {pid} 위치가 예상과 다릅니다.')
        return off,bs,sz,tid

    # object 3174: apply staged dialogue edits while consuming existing alignment gap
    off,bs,sz,_=obj_info(3174);offn,bsn,szn,_=obj_info(3175)
    s=data_offset+bs;nexts=data_offset+bsn;obj=bytearray(level[s:s+sz]);base_size=sz
    # 찾아버렸네 -> 들켜버렸네 (2 occurrences including '또 ...')
    obj,_=fixed_replace(obj,'찾아버렸네!','들켜버렸네!',2)
    rewrite_fixed_serialized_string(obj,'있잖아, 알아?','있잖아 그거 알아')
    obj,g=replace_serialized_string(obj,'결정이야!','하기로 한거야')
    obj,g2=replace_serialized_string(obj,'하기로 한거야','하기로 한거야!')
    obj,g3=replace_serialized_string(obj,'있잖아 그거 알아','있잖아, 그거 알아?')
    rewrite_fixed_serialized_string(obj,'그럼 오늘도 부탁해!','그럼 오늘도 하자!')
    rewrite_fixed_serialized_string(obj,'모르는 사람을 빤히 보지 말고','모르는 사람을 쳐다 보지 말고')
    obj,_=fixed_replace(obj,'모르는 사람을 쳐다 보지 말고','모르는 사람은 쳐다 보지 말고',1)
    growth=len(obj)-base_size;gap=nexts-(s+base_size)
    if growth>gap:raise RuntimeError('대사 오브젝트 확장 공간이 부족합니다.')
    level[s:nexts]=obj+level[s+base_size+growth:nexts]
    struct.pack_into('<I',level,off+16,len(obj))

    # speaker 男 -> 남자, grows into 4-byte gap
    off,bs,sz,_=obj_info(3227);offn,bsn,_,_=obj_info(3228);s=data_offset+bs;nexts=data_offset+bsn
    obj=bytearray(level[s:s+sz]);pos=obj.find('男'.encode());
    if pos<4:raise RuntimeError('男 화자 라벨을 찾지 못했습니다.')
    lp=pos-4;decl=struct.unpack_from('<I',obj,lp)[0];oa=(pos+decl+3)&~3;nb='남자'.encode();nf=struct.pack('<I',len(nb))+nb+b'\0'*((4-len(nb)%4)%4)
    nobj=obj[:lp]+nf+obj[oa:];growth=len(nobj)-len(obj)
    if growth>nexts-(s+sz):raise RuntimeError('男 라벨 확장 공간 부족')
    level[s:s+len(nobj)]=nobj;struct.pack_into('<I',level,off+16,len(nobj))

    # speaker 先生 -> 선생님; shift object 3240 into its following gap
    off,bs,sz,_=obj_info(3239);off40,bs40,sz40,_=obj_info(3240);off41,bs41,_,_=obj_info(3241)
    s=data_offset+bs;s40=data_offset+bs40;s41=data_offset+bs41;obj=bytearray(level[s:s+sz]);pos=obj.find('先生'.encode())
    if pos<4:raise RuntimeError('先生 화자 라벨을 찾지 못했습니다.')
    lp=pos-4;decl=struct.unpack_from('<I',obj,lp)[0];oa=(pos+decl+3)&~3;nb='선생님'.encode();nf=struct.pack('<I',len(nb))+nb+b'\0'*((4-len(nb)%4)%4)
    nobj=obj[:lp]+nf+obj[oa:];growth=len(nobj)-len(obj);obj40=bytes(level[s40:s40+sz40])
    if growth>s41-(s40+sz40):raise RuntimeError('先生 라벨 확장 공간 부족')
    level[s:s+len(nobj)]=nobj;level[s40+growth:s40+growth+sz40]=obj40
    struct.pack_into('<I',level,off+16,len(nobj));struct.pack_into('<Q',level,off40+8,bs40+growth)

    # Man's long call is already translated by base pair おいって！！ -> 야!!.
    # Keep girl's おーい -> 어이! intact.
    logical[level_off:level_off+level_size]=level
    return build_bundle(bun,logical)

def _progress_bar(label, current, total=None, width=30):
    if total and total > 0:
        ratio = min(1.0, current / total)
        filled = int(width * ratio)
        bar = "█" * filled + "░" * (width - filled)
        pct = ratio * 100
        text = f"\r{label} [{bar}] {pct:5.1f}%  {current / 1024 / 1024:6.1f}/{total / 1024 / 1024:6.1f} MB"
    else:
        text = f"\r{label} {current / 1024 / 1024:6.1f} MB 다운로드 중..."
    print(text, end="", flush=True)

def download(url, label="다운로드"):
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://unityroom.com/'
        }
    )
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(req, timeout=60, context=ssl_context) as r:
        total_header = r.headers.get("Content-Length")
        total = int(total_header) if total_header and total_header.isdigit() else None

        chunks = []
        received = 0
        chunk_size = 256 * 1024

        _progress_bar(label, 0, total)

        while True:
            chunk = r.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            _progress_bar(label, received, total)

    print()
    data = b"".join(chunks)

    if data[:2] == b'\x1f\x8b':
        print(f"{label}: 압축 해제 중...", flush=True)
        data = gzip.decompress(data)

    print(f"{label}: 완료 ({len(data) / 1024 / 1024:.1f} MB)", flush=True)
    return data

def patch_web(web,ttf):
    # only warn on hash mismatch; downloader may return identical decompressed bytes under a different transfer encoding
    h=sha256(web)
    if h!=EXPECTED_WEB_SHA:
        print(f'주의: 원본 webgl.data 해시가 예상과 다릅니다: {h}')

    print("  (1/5) Unity 데이터 읽는 중...", flush=True)
    bundle=extract_bundle(web)

    print("  (2/5) 한국어 대사 적용 중...", flush=True)
    bundle=patch_initial_dialogue(bundle)

    print("  (3/5) 한글 폰트 적용 중...", flush=True)
    bundle=patch_font(bundle,ttf)

    print("  (4/5) 추가 번역 수정 적용 중...", flush=True)
    bundle=patch_extras(bundle)

    print("  (5/5) 게임 데이터 다시 만드는 중...", flush=True)
    result=rebuild_webdata(web,bundle)

    print("  패치 적용 완료", flush=True)
    return result


INDEX_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>夕日のかえりみち - 한국어 패치</title>
<style>
  html,body { margin:0; min-height:100%; background:#111; }
  body { display:flex; justify-content:center; align-items:flex-start; padding:24px 16px; box-sizing:border-box; }
  #player { width:800px; max-width:96vw; }
  #unity-canvas { display:block; width:800px; height:600px; max-width:96vw; background:#000; }
  #status { color:#ddd; font:13px sans-serif; margin-top:8px; text-align:center; }
</style>
</head>
<body>
<div id="player">
  <canvas id="unity-canvas" width="960" height="600" tabindex="-1"></canvas>
  <div id="status">Unity 로딩 준비 중…</div>
</div>
<script src="webgl.loader.js"></script>
<script>
const canvas = document.querySelector("#unity-canvas");
const status = document.querySelector("#status");
createUnityInstance(canvas, {
  dataUrl:"webgl.data?v=release1",
  frameworkUrl:"webgl.framework.js?v=release1",
  codeUrl:"webgl.wasm?v=release1",
  streamingAssetsUrl:"StreamingAssets",
  companyName:"Local Patch",
  productName:"Yuhino Kaerimichi Korean Patch",
  productVersion:"1.0",
  showBanner:(msg,type)=>{ console[type==="error"?"error":"warn"](msg); status.textContent=msg; }
}, p => status.textContent=`로딩 중… ${Math.round(p*100)}%`)
.then(x => { window.unityInstance=x; status.textContent="실행 완료"; })
.catch(e => { console.error(e); status.textContent="실행 오류 — Console 확인"; });
</script>
</body>
</html>
"""

def save_download(url, path, label=None):
    data = download(url, label or path.name)
    path.write_bytes(data)
    return len(data)

def _resource_dir() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))

def _user_data_dir() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home())) / "YuhiKaerimichiKoreanPatch"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "YuhiKaerimichiKoreanPatch"
    return Path.home() / ".local" / "share" / "YuhiKaerimichiKoreanPatch"

def _valid_original_cache(path: Path):
    if not path.exists():
        return False
    try:
        data = path.read_bytes()
        return sha256(data) == EXPECTED_WEB_SHA
    except Exception:
        return False

def _runtime_ready(game_dir: Path):
    return all((game_dir / name).exists() for name in (
        "webgl.loader.js", "webgl.framework.js", "webgl.wasm"
    ))

def prepare_game(root: Path | None = None, source_webgl: Path | None = None, patch_only: bool = False):
    base_dir = _user_data_dir()
    game_dir = base_dir / "game"
    cache_dir = base_dir / "cache"
    game_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    font_path = _resource_dir() / "korean_font.ttf"
    if not font_path.exists():
        raise RuntimeError("내장 한글 폰트를 찾을 수 없습니다.")

    patched_path = game_dir / "webgl.data"
    marker_path = game_dir / "patch_version.txt"
    original_cache = cache_dir / "original_webgl.data"

    # If this exact patch version was already generated, skip download + patch completely.
    if (
        patched_path.exists()
        and marker_path.exists()
        and marker_path.read_text(encoding="utf-8", errors="ignore").strip() == PATCH_VERSION
    ):
        print("\n[1/4] 기존 한국어 패치 데이터 사용 ✓", flush=True)
        print("[2/4] 패치 적용 생략 ✓", flush=True)
    else:
        print("\n[1/4] 원본 게임 데이터 준비", flush=True)

        if source_webgl:
            web = source_webgl.read_bytes()
            if web[:2] == b"\x1f\x8b":
                web = gzip.decompress(web)
        elif _valid_original_cache(original_cache):
            print("원본 게임: 캐시 사용 ✓", flush=True)
            web = original_cache.read_bytes()
        else:
            web = download(DATA_URL, "원본 게임")
            if sha256(web) == EXPECTED_WEB_SHA:
                original_cache.write_bytes(web)
                print("원본 게임: 다음 실행을 위해 캐시에 저장 ✓", flush=True)

        print("\n[2/4] 한국어 패치 적용", flush=True)
        patched = patch_web(web, font_path.read_bytes())
        patched_path.write_bytes(patched)
        marker_path.write_text(PATCH_VERSION, encoding="utf-8")

    if patch_only:
        print(f"완료: {patched_path}")
        return game_dir

    print("\n[3/4] 실행에 필요한 파일 준비", flush=True)

    # Download only missing runtime files. Existing ones are reused.
    jobs = [
        (LOADER_URL, game_dir / "webgl.loader.js", "로더"),
        (FRAMEWORK_URL, game_dir / "webgl.framework.js", "프레임워크"),
        (WASM_URL, game_dir / "webgl.wasm", "게임 엔진"),
    ]
    missing = [(u, p, l) for u, p, l in jobs if not p.exists()]

    if not missing:
        print("실행 파일: 기존 파일 사용 ✓", flush=True)
    else:
        # Download independent runtime files in parallel to reduce total wait time.
        from concurrent.futures import ThreadPoolExecutor, as_completed
        print(f"실행 파일 {len(missing)}개 병렬 다운로드 중...", flush=True)
        with ThreadPoolExecutor(max_workers=min(3, len(missing))) as ex:
            futures = {
                ex.submit(save_download, url, path, label): label
                for url, path, label in missing
            }
            for fut in as_completed(futures):
                fut.result()

    (game_dir / "index.html").write_text(INDEX_HTML, encoding="utf-8")

    print("\n[4/4] 준비 완료 ✓", flush=True)
    return game_dir

def serve(game_dir: Path):
    import http.server, socketserver

    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {
            **http.server.SimpleHTTPRequestHandler.extensions_map,
            ".wasm": "application/wasm",
            ".js": "text/javascript",
            ".data": "application/octet-stream",
        }

    old_cwd = os.getcwd()
    os.chdir(game_dir)
    try:
        port = None
        httpd = None
        for candidate in range(8000, 8011):
            try:
                httpd = socketserver.ThreadingTCPServer(("127.0.0.1", candidate), Handler)
                port = candidate
                break
            except OSError:
                continue
        if httpd is None:
            raise RuntimeError("8000~8010 포트를 사용할 수 없습니다.")

        url = f"http://127.0.0.1:{port}/"
        print()
        print("한국어판 실행:", url)
        print("종료하려면 이 터미널에서 Ctrl+C를 누르세요.")
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
        finally:
            httpd.server_close()
    finally:
        os.chdir(old_cwd)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="夕日のかえりみち 한국어 패치 자동 설치/실행기")
    ap.add_argument("--source-webgl", type=Path, help="테스트/오프라인용 원본 webgl.data 경로")
    ap.add_argument("--patch-only", action="store_true", help="패치된 webgl.data만 생성하고 서버 실행은 생략")
    args = ap.parse_args()

    game_dir = prepare_game(None, args.source_webgl, args.patch_only)
    if not args.patch_only:
        serve(game_dir)

if __name__ == "__main__":
    main()
