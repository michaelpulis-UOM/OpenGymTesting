from tempfile import TemporaryFile
import bisect
import glob
import numpy as np 
import json
import math
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt

class CreateDataset():
    
    def __init__ (self):
        # Initialising Class Variables
        self.PASS = 0
        self.SHOOT = 1
        self.CARRY = 2
        self.CLEAR = 3
        self.FOUL = 4

        self.lim = 5

        self.xT_Map = [[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007062146892655163, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00036845983787767064, 0.0, 0.0038387715930902153, 0.0032154340836012887, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0006898930665746804, 0.001639344262295082, 0.01511627906976744, 0.021612635078969242, 0.015957446808510634], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000630119722747291, 0.0, 0.0, 0.00045146726862302204, 0.0009372071227741336, 0.007127583749109053, 0.025599999999999998, 0.08403361344537814, 0.10552763819095476], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009638554216867468, 0.01359223300970874, 0.05, 0.140625, 0.3931034482758621], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0026881720430107516, 0.005550416281221091, 0.07714701601164484, 0.14393939393939395, 0.3538961038961039], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00293398533007335, 0.004971002485501242, 0.029929577464788727, 0.08356940509915013, 0.1116751269035533], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00035075412136091144, 0.0012155591572123182, 0.002170767004341534, 0.00980392156862745, 0.020642201834862386, 0.012084592145015107], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004775549188156536, 0.0, 0.0007656967840734922, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [[1.0366556234347302e-05, 2.4310709439662652e-05, 1.4889692589620287e-05, 6.109952011345943e-05, 6.0078065832173205e-05, 7.427346470154124e-05, 0.00015199873058314122, 0.00018267206713613635, 0.0004151596937826378, 0.0006559578939930636, 0.0010026195229035366, 0.002046902916127498, 0.007016557353851138, 0.010469747814695701, 0.015270023750327396, 0.01797328565756389], [1.3326472954851575e-05, 9.387750024870354e-05, 3.610685257907658e-05, 0.00015874427428968964, 5.829377000760303e-05, 6.048105286295511e-05, 0.00023897963284320154, 0.0003611126890551234, 0.0005215002170858285, 0.000944786274882627, 0.001855066637153107, 0.004154886196286874, 0.008441191706083515, 0.013577689988766786, 0.025018383013846707, 0.041354985832976546], [3.135189365437653e-06, 3.0501997780374275e-05, 2.006022968995803e-05, 8.13878106371928e-05, 7.597862954123621e-05, 0.00015920632040237348, 0.0002521273990289451, 0.0006671740261903096, 0.00029309580548784596, 0.000748192477088049, 0.0019895561443879104, 0.0060027166540799395, 0.009770834625280785, 0.020904572519351045, 0.040771687356089256, 0.04461577531023448], [3.2497391408921534e-05, 4.74336181659794e-05, 0.0001643807217846907, 9.18074427899602e-05, 3.6415676369311846e-05, 0.00015735119375378896, 0.00021713891727254023, 0.0004290945503708691, 0.0005783509748255473, 0.001046292946339317, 0.0025373817732650353, 0.006305530510749755, 0.011387099845511091, 0.032599640787268104, 0.05150845021339909, 0.0798129541686833], [4.205316721708023e-05, 0.00012372433552563695, 0.00011978591621930261, 0.00016242817980070972, 0.00010393219416420794, 0.000138002969784355, 0.00017986008541763347, 0.001069553711586827, 0.0006712138413429347, 0.0008537380206409706, 0.0033749929553890806, 0.006252009629129382, 0.019501174007107023, 0.044868720896601724, 0.10999663290773759, 0.1471387386217682], [2.840806719722706e-05, 6.465002025239652e-05, 0.0002636907662282423, 4.495526882452603e-05, 5.830043018496166e-05, 0.00011372234940077737, 0.00027876129006911156, 0.0002718659550370981, 0.0005898482534523136, 0.0011500017411153762, 0.0030226500816187634, 0.007042412830805462, 0.0260631329661805, 0.07132752340916654, 0.162882538742887, 0.4096778819295067], [5.055806073893027e-05, 0.00018541750101774558, 0.00030551064425759285, 6.491245013062614e-05, 8.69933060010856e-05, 6.63924389717408e-05, 0.0003331284423972193, 0.0003349467384571337, 0.0008221387889580194, 0.0018678985381715386, 0.0029532543675532268, 0.008477745297757858, 0.016712862795729075, 0.09871189156245068, 0.16589839555373795, 0.3681911084557573], [4.8327319386158817e-05, 6.49704914938541e-05, 0.00013048567307101427, 0.00025082960042796846, 7.957907387892639e-05, 0.0001839301853411982, 0.00014568489621072904, 0.00045553551657889866, 0.0008313792571913091, 0.0013130318427521414, 0.0030369739100087217, 0.008780250325811966, 0.016309587046132928, 0.050643352651302515, 0.10790124499418861, 0.1448650530444383], [8.519911566015381e-05, 0.00018711323309351867, 9.036821488641698e-05, 0.0001435592390311494, 4.905352181137975e-05, 0.00015577103474483366, 0.0003717986595449662, 0.0003459306918260699, 0.0006924910738880948, 0.0009583285936289216, 0.0028346700383334923, 0.007095407709936382, 0.01201436419475773, 0.02713429317917297, 0.05421982122639214, 0.08347001986230133], [9.550690723007499e-06, 5.69322229600752e-05, 3.2809535363772726e-05, 4.009449966613987e-05, 9.589910087237808e-05, 0.00018200885901222753, 0.00029866400955201497, 0.0006537180810314532, 0.0009567044509506458, 0.0008300729043258944, 0.002584467516876723, 0.006514769734102766, 0.011133214387950015, 0.01839566476918161, 0.03873276589370377, 0.08336024215381267], [4.739920558931236e-06, 1.432056320613839e-05, 3.1246634108049806e-05, 5.659266636201608e-05, 6.667584988861055e-05, 0.0002850401685112207, 0.0003199313034729257, 0.000451318988227541, 0.0003779694686327631, 0.0007696632895442547, 0.002138244878651422, 0.004926203522240533, 0.009638091584880555, 0.015013666772934791, 0.025583102394128306, 0.04011412273717388], [0.0, 4.839307748269079e-06, 5.26645542830565e-05, 4.789561699789742e-05, 9.783166270269824e-05, 9.051243321370137e-05, 0.00015089885288419792, 0.00018269708023795214, 0.0003262001706165189, 0.0006481906440299153, 0.0013115591929206798, 0.002320219592734313, 0.0063050660114200695, 0.011929876725490632, 0.015418092171414202, 0.01869625399741503]], [[0.00031976451877803946, 0.00041145690210536777, 0.00030335152073632644, 0.0006404895660564677, 0.0005781385304833165, 0.0008615351914149853, 0.0012539713987216516, 0.0014352649312604053, 0.0022537171619812784, 0.003265062423929327, 0.004840795114843465, 0.00831265105688004, 0.016609924653151767, 0.023760324672212053, 0.03275786915781487, 0.03751059408938904], [0.00021435788154235873, 0.0011078669805708187, 0.0005763657004157376, 0.0007336341032572373, 0.0006262192538424034, 0.0007997388399377608, 0.0012477772933069552, 0.0018040772513164187, 0.00251326228003161, 0.0038018908938275446, 0.0064174697500785065, 0.011665675462981112, 0.02000821650566636, 0.02986018261531575, 0.046793075263048614, 0.06495617438635924], [0.00021668916219987815, 0.0004133228504232201, 0.0003205071879447536, 0.0005127079859647053, 0.0005471723856118197, 0.0009934581962771321, 0.001315607843610978, 0.002249592917325275, 0.002388876658555324, 0.004021702995904987, 0.007347572295712763, 0.015233815110281506, 0.02292661548955279, 0.0406621567800162, 0.0671706786343634, 0.07501144331927552], [0.00035138294889414015, 0.000579096853069008, 0.0007583060829301204, 0.0005617057442073084, 0.0005133393609770985, 0.0009273921415940217, 0.0012386057688927327, 0.0018726258068182862, 0.002856741747236562, 0.004244521237092559, 0.00805405183477807, 0.015377958106561887, 0.023981088723922295, 0.048979514374067494, 0.07175658774015857, 0.10459580300115266], [0.0006461490367296954, 0.0007086466383138105, 0.0010067046484134846, 0.0007018867003050263, 0.0006017663169538132, 0.0009434752817846702, 0.0012744786767443603, 0.0027010155692063663, 0.003166425216215684, 0.004436664234273775, 0.009173488415983618, 0.014752875343202708, 0.03109806511766228, 0.05651954935169844, 0.11934036326771758, 0.1541623419856828], [0.0005051410752578062, 0.0007269717713796652, 0.0013199843065038119, 0.0005233125839434551, 0.0005996511914451831, 0.0008353825012262157, 0.0013984984794705824, 0.0018088738248499608, 0.0031149396661075304, 0.004663927282137632, 0.009106946571165148, 0.015739873498785698, 0.036646970685397934, 0.08043001250967577, 0.16799275443221795, 0.4116357550712247], [0.0005991901906267843, 0.0008161455195620353, 0.0014359466777545118, 0.0006744511192605504, 0.0006539607590331971, 0.0007216655494388824, 0.001480485464935036, 0.001991209303082345, 0.003134256916760575, 0.005771833366359677, 0.008995603664794133, 0.017024832566102484, 0.027104342720765208, 0.10775351574768, 0.17176806969328412, 0.3699425170712099], [0.0006215357634839519, 0.000824368097682311, 0.0012026825713018433, 0.0008269468047025941, 0.0006592916885060428, 0.0008782545533402072, 0.0013699415334535096, 0.0020370540149307614, 0.003555008875667676, 0.005325506090792361, 0.008735650984630626, 0.018196829666705546, 0.02867530887681041, 0.06392545120749471, 0.1170247866051085, 0.1532881933494386], [0.0007134017558131652, 0.0007049628229305096, 0.0006895263669140251, 0.0005784871797242374, 0.0005767839942605195, 0.0009272606307184758, 0.001625207679642894, 0.0017612706283271801, 0.0029872958040941377, 0.004470980010572425, 0.008641116730723052, 0.016434439125569605, 0.026149244037443564, 0.0451950964186352, 0.07721150576452596, 0.10841324319467546], [0.00029730094577472065, 0.0006054222503596322, 0.0004647311253127656, 0.0004457747860105772, 0.0006792019136034435, 0.0010580559427619328, 0.001590981786132267, 0.002449773182519606, 0.0032997203152245495, 0.004067413565483222, 0.008226930976914718, 0.01598954606803912, 0.025485642789710338, 0.04022313361361992, 0.06848848352057323, 0.1129913777356024], [0.00023148330908743484, 0.00036782934474824467, 0.0005472352159851313, 0.0005801253048753743, 0.0006646284578451879, 0.001230064935770662, 0.0016833700476342364, 0.0022121405436338324, 0.0026571175546419835, 0.003792490755962877, 0.007163064620168702, 0.012788083190167873, 0.021404510605804134, 0.03315853863164579, 0.047859551644236456, 0.0659316633906435], [0.00016904972965748, 0.00023015523765301227, 0.0004617217822350958, 0.0005694952910405263, 0.0006794015402706961, 0.0009111189477214957, 0.0012748865532977653, 0.0015869768106485207, 0.0023573996332342776, 0.0036026070995463216, 0.0056350725723134385, 0.008858957816832647, 0.017229032001740748, 0.026260100011639385, 0.03415459452268048, 0.03895559658400106]], [[0.001235151785646206, 0.0015268351503895273, 0.0013342572799367107, 0.0019593240871500937, 0.001976219666192071, 0.0025886123294150726, 0.003495833776645022, 0.0040168802198665525, 0.005713095324879622, 0.007702483873803587, 0.010737695139233268, 0.016307315448818728, 0.026883668622727768, 0.0364897447372612, 0.047675503919722396, 0.05336542933769526], [0.0010441977582299742, 0.0026623177454708005, 0.0018553289679569143, 0.0020180973602130945, 0.0020330918486874076, 0.002546498451122924, 0.003392199416392903, 0.0045333482181392215, 0.006239129276121391, 0.008635438748476965, 0.012956152410238661, 0.020547880838940685, 0.031551258056395436, 0.04427402033797533, 0.06313968206530904, 0.08072254863525838], [0.0010161189745554057, 0.0014477876226412088, 0.0013506282638711205, 0.0016451666186720467, 0.0018380398322472233, 0.0027859491779853333, 0.003590609865804061, 0.0052073427077244565, 0.006310843605796943, 0.009221111489834668, 0.014578278152760749, 0.025154629571526633, 0.03523857461262286, 0.055872133101580436, 0.08356405778218395, 0.0920838926872662], [0.0014576129962752273, 0.001969062039643792, 0.002113547345955074, 0.001728439131861172, 0.001799915217845405, 0.002721120473101994, 0.0035224351418942745, 0.004759486199318907, 0.006996243280240641, 0.00942854912252609, 0.015283907127659055, 0.025087369351567638, 0.03491913926473979, 0.06009980397821494, 0.08274769312101261, 0.11653254308063124], [0.002194804078635748, 0.002233756270336503, 0.0028986060165502804, 0.001993837076893899, 0.001932657532896675, 0.002785506818587873, 0.0036204014519834035, 0.005802717135438259, 0.007576161336121524, 0.010196452039094198, 0.01669158304999433, 0.023939215099021423, 0.040590884341559316, 0.0633756038335497, 0.12352196399730211, 0.15663289175109674], [0.0018668695348939418, 0.002352208769239108, 0.003481936451976487, 0.001755092381865559, 0.001971355931152263, 0.0026173745210551756, 0.003830877762649286, 0.004847017099082038, 0.007474264446334985, 0.010320874058506312, 0.01689195353252045, 0.02493472250099337, 0.04506542836891399, 0.08546874084742924, 0.16999328928812754, 0.4123636676654068], [0.001977477530756963, 0.0024263113025182444, 0.003665083459127091, 0.002134115730816247, 0.0020697610881118093, 0.0024397342919879905, 0.003938383545575528, 0.005168731227584441, 0.007129819541199598, 0.011679832188831686, 0.016773425105288394, 0.026173144847404118, 0.0355211673373847, 0.11271354047370463, 0.17432413201350414, 0.3706766366187927], [0.0021825754621114467, 0.00266432440018163, 0.0035089204548937976, 0.0021980139955854548, 0.0020865817727583023, 0.0026295984886048262, 0.003904429460906426, 0.005101952939383506, 0.008166651987786351, 0.011259088529810527, 0.01637133639494085, 0.02789924394139014, 0.03867325841174163, 0.07214429022809214, 0.1213448148485053, 0.1562893084687605], [0.0020137485173346227, 0.002135154605547064, 0.0021281960331119808, 0.0017764732454277113, 0.0019592121589833743, 0.002781202806842459, 0.004129093109917101, 0.004706236352507063, 0.00719322303020925, 0.009980843402043763, 0.016315137656420422, 0.026337351869703245, 0.037826131149865744, 0.05741972039313285, 0.0892295376854645, 0.11960147398518485], [0.0013158775474207218, 0.0018186929175714637, 0.0016087364473654476, 0.0015644523301945401, 0.0021211935817022787, 0.0029238051891730694, 0.004176509616851133, 0.00568315587252441, 0.0073550524305686284, 0.009407189936795976, 0.015614437078638667, 0.026120565708692506, 0.038441605137241514, 0.05626264442156369, 0.08547395379494185, 0.12742745344024067], [0.00102910722719872, 0.0014285047469535673, 0.0018158184236996742, 0.0019225545894766432, 0.002169069405941567, 0.0031873890514952756, 0.004281077851100364, 0.005303237596252633, 0.0067070485093339485, 0.008798707949517679, 0.01408465580122822, 0.022047748531869117, 0.03339686316387158, 0.04834189546102216, 0.06451009874061067, 0.0823625754849612], [0.0008943558817821355, 0.0010899618968721273, 0.0016287483119557947, 0.0019276954083512052, 0.002166608583269355, 0.002773162213076601, 0.0036646889510341843, 0.004353747189452802, 0.006131144639471409, 0.008401149074815704, 0.012075741977501817, 0.017340026161523952, 0.028568450013029264, 0.03974903817256651, 0.05003854238442088, 0.055321421611592037]], [[0.002960039308068086, 0.0035229730548060434, 0.0033020407487492926, 0.004202145696688671, 0.004392467457137216, 0.005365147912260797, 0.006848865799864279, 0.0078005533633671255, 0.01043721060068205, 0.013335628831457995, 0.017658558261337835, 0.02470358102156615, 0.03662222831059948, 0.0476015078735218, 0.05975949451389147, 0.06578557716874991], [0.002756912333805984, 0.004942945776111035, 0.004002338302718488, 0.004213942247346128, 0.004437525145669757, 0.005390506994099158, 0.0066885414784960216, 0.008470566396291054, 0.011263812113335513, 0.014686857707460699, 0.0203497625763559, 0.029470756750073757, 0.04190817889002741, 0.0560430535638623, 0.07527311711431932, 0.09197373780131499], [0.0026869302719023584, 0.003367294864057422, 0.003356314765000063, 0.0037110935906275455, 0.004153477054877673, 0.005666352089059111, 0.007075342605808902, 0.009395673733627588, 0.011551967058043558, 0.015552895881508117, 0.022405187346919413, 0.034450093013649374, 0.045618277672443495, 0.06690585088593891, 0.09416450426794981, 0.10250460133078065], [0.0035896899035147856, 0.0043432265690069236, 0.0043860968311141375, 0.0038135352991069947, 0.004117501999607568, 0.005660723421682172, 0.007074343629816964, 0.008956986181593414, 0.01246694636518069, 0.01580693003674537, 0.02306735201040512, 0.03410357786492534, 0.04367387915154575, 0.06758100591616756, 0.08926881048496729, 0.12343150328049621], [0.004789158102741685, 0.004785558629446031, 0.0057807766926603645, 0.004229897950247681, 0.004316847763310467, 0.005778081494675143, 0.007235331279001224, 0.010224522380771235, 0.0132873230115501, 0.01704135999624356, 0.024666634662071866, 0.03250499447568692, 0.04797052468739965, 0.06770993036569728, 0.12583011438690617, 0.15790747789992735], [0.0042329046648028855, 0.005010678345039706, 0.0066430974705279835, 0.0039451614540006955, 0.004397979223136659, 0.00557800852468157, 0.007533000753900857, 0.009232868946461234, 0.013094487446159028, 0.0171339001848333, 0.02504395388961446, 0.03339953560065757, 0.05158936719688724, 0.08876171318587878, 0.17106000601333948, 0.41276951923166083], [0.004389079347344928, 0.005099633527886411, 0.006887813357554737, 0.004581975043167565, 0.004521803667979526, 0.005335870687609309, 0.007696914355770025, 0.009659820315821861, 0.012376589107375128, 0.018617900178941136, 0.024917154399247844, 0.03458397081663608, 0.04204502842441574, 0.11587610886550147, 0.17575393751765955, 0.37113671326717484], [0.004829508547200144, 0.005588992643518123, 0.0068747478507284075, 0.004542015028617974, 0.004570753224709054, 0.005561902438573788, 0.007699273245876033, 0.009489502347848372, 0.014026569359773422, 0.01816221863729818, 0.0244758632953303, 0.036702055892731046, 0.046341670988162637, 0.0774530662993117, 0.12374932385083384, 0.1578198100605594], [0.004304222527694321, 0.004632465152483658, 0.004532728508702042, 0.003960303280363443, 0.004385836346240944, 0.005815389711457576, 0.007848096228974887, 0.009015508338404424, 0.012757944572593893, 0.01660788261236281, 0.024454593678020508, 0.035503687326550494, 0.046846230993670586, 0.06541013764418088, 0.09610464599298624, 0.1258531991998774], [0.003301486160804869, 0.003957617659540504, 0.003691345603321024, 0.0036460579761116714, 0.004593752327059179, 0.005905069475762588, 0.007967593288141117, 0.010119437046116514, 0.01268789348623038, 0.015922576112294924, 0.02356958538437995, 0.035624008995684915, 0.04907666724135731, 0.0675889852313226, 0.09606561149264668, 0.13603932109632816], [0.0026824032395953512, 0.0034195508030779604, 0.004025391988138384, 0.004248086295966303, 0.004721274732485909, 0.006222474109619849, 0.008007474278684033, 0.00953848681037967, 0.011989649941497312, 0.014985988854057783, 0.021744456463248137, 0.031255576184710636, 0.04410013725497966, 0.06031013242501252, 0.0767763096116025, 0.09367268896304817], [0.0024930409059009027, 0.002879505090517776, 0.003766593820647327, 0.004283048813856103, 0.004712266997785805, 0.005749517434545514, 0.007214026955682827, 0.00832861944982618, 0.011172020190545499, 0.014368918630045477, 0.019431657286749143, 0.02617435579949552, 0.039015712517662234, 0.05122993400995453, 0.06255972119801648, 0.06791558867412512]]]
        self.xT_Map = np.array(self.xT_Map[5])

        self.possession_limit = 5

        self.games = None
        self.events = None
        self.ids = {}
        self.good_events = {
            
            'pass': self.PASS,
            'shot': self.SHOOT,
            'carry':self.CARRY,
            'clearance':self.CLEAR,
            # 'foul won': self.FOUL,
            # 'foul': self.FOUL,

        }

        self.file_limit = -1
        
        self.ID_to_str = { v:k for k,v in self.good_events.items()}

        self.tracking_content = {}
        self.games_with_tracking = {}

    def filter_game(self, dataset):
        return [ 
            a for a in dataset 
            if  ('type' in a)
            and (a['type']['name'].lower() in self.good_events) 
            and ('location' in a)
        ]
            
    def getIDFromAction(self, item):
        return 1.0 * self.good_events[item['type']['name'].lower()]


    def get_index_of_event(self, event):
        _id = event['id']
        for i, event in enumerate(self.events):
            if(event['id'] == _id): return i

        return -1

    def get_zone_from_coords(self, x, y):
        rows = self.xT_Map.shape[0]
        cols = self.xT_Map.shape[1]

        zone_0 = int((y/80) * rows)
        zone_1 = int((x/120) * cols)

        return min(zone_0, rows-1), min(zone_1, cols-1)

    def get_xt_diff(self, event, next_event):

        zone_0, zone_1 = self.get_zone_from_coords(event["location"][0], event["location"][1])
        current_xt = self.xT_Map[zone_0][zone_1]

        zone_0, zone_1 = self.get_zone_from_coords(next_event["location"][0], next_event["location"][1])
        next_xT = self.xT_Map[zone_0][zone_1]

        return next_xT - current_xt

    def calculate_reward(self, event, next_event):

        # Return xG if a shot is taken
        if(event['type'] == "shot"):
            return event['shot']['statsbomb_xg']

        # Lost possession with the current action
        if(event['team']['id'] != next_event['team']['id']):
            return -1
        
        if(event['type'] == "foul"):
            return 0.5 # TODO: CHANGE THIS
        else:
            # Return the different in xT generated by the event (pass or carry)
            return self.get_xt_diff(event, next_event)
        
    def get_XT_Zone(self, event):
        coords = event['location']    
        zones = self.get_zone_from_coords(coords[0], coords[1])

        return zones


    def getDistanceBetweenPlayers(self, l1, l2):
        return math.sqrt((l1[0] - l2[0])**2 + (l1[1] - l2[1] )**2)

    def getPlayersPerRadius(self, frame, center, radii=[10, 40, 80]):

        team_zone_count = [0 for i in range(len(radii) + 1)]
        oppo_zone_count = [0 for i in range(len(radii) + 1)]

        for player in frame['freeze_frame']:

            if player['actor']: continue

            distance = self.getDistanceBetweenPlayers(center, player['location'])

            
            if player['teammate']:
                team_zone_count[bisect.bisect(radii, distance)] += 1
            elif not player['teammate']:
                oppo_zone_count[bisect.bisect(radii, distance)] += 1

        return team_zone_count, oppo_zone_count

    def getPlayersPerZone(self, frame):

        rows = self.xT_Map.shape[0]
        cols = self.xT_Map.shape[1]

        team_players_per_zone = np.zeros((rows,cols), dtype=np.uint)
        oppo_players_per_zone = np.zeros((rows,cols), dtype=np.uint)

        for player in frame['freeze_frame']:

            # if player['actor']: continue

            x, y = player['location'][0], player['location'][1]
            r, c = self.get_zone_from_coords(x, y)
            
            if player['teammate']:
                team_players_per_zone[r][c] += 1
            elif not player['teammate']:
                oppo_players_per_zone[r][c] += 1

        return team_players_per_zone, oppo_players_per_zone

    def plot(self, x,y,z,grid):
        # plt.figure()
        
        plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()), cmap='jet')
        plt.scatter(x,y,c=z, cmap='jet')

        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                    hspace = 0, wspace = 0)

        plt.margins(0,0)
        plt.savefig("myfig.png",  bbox_inches = 'tight', transparent = True, pad_inches=0)
        plt.clf()

        return cv2.imread("myfig.png")  

    def distance_matrix(self, x0, y0, x1, y1):
        obs = np.vstack((x0, y0)).T
        interp = np.vstack((x1, y1)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = np.subtract.outer(obs[:,0], interp[:,0])
        d1 = np.subtract.outer(obs[:,1], interp[:,1])

        return np.hypot(d0, d1) * 2

    
    def getWeightedFromArrays(self, x,y,z):
        nx = 120 
        ny = 80

        x=np.array(x)
        y=np.array(y)
        z=np.array(z)

        xi = np.linspace(x.min(), x.max(), nx)
        yi = np.linspace(y.min(), y.max(), ny)
        xi, yi = np.meshgrid(xi, yi)
        xi, yi = xi.flatten(), yi.flatten()

        dist = self.distance_matrix(x,y, xi,yi)

        # In IDW, weights are 1 / distance
        weights = 1 / dist

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, z)
        zi = zi.reshape((ny, nx))

        zi = np.nan_to_num(zi)
        _max = np.min(zi)
        _min = np.max(zi)

        # get_space_bet_nums
        diff = _max - _min

        zi = (zi - _min) / diff
        return zi    

    def drawIDW(self, frame):

        x , y, z = [], [], []

        nx = 120 
        ny = 80

        x.append(0)
        x.append(nx)
        x.append(0)
        x.append(nx)

        y.append(0)
        y.append(0)
        y.append(ny)
        y.append(ny)

        z.append(0)
        z.append(0)
        z.append(0)
        z.append(0)


        actor_x, actor_y = -1, -1

        for player in frame['freeze_frame']:
            if(player['actor']):
                actor_x = int(player['location'][0])
                actor_y = int(player['location'][1])
                


            x_t = int(player['location'][0] )
            y_t = int(player['location'][1] )
            z_t = -1 if player['teammate'] else 1
            
            x.append(x_t)
            y.append(y_t)
            z.append(z_t)

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        zi = self.getWeightedFromArrays(x, y, z)
        zi = zi ** 2

        just_actor_image = np.zeros(zi.shape)
        cv2.circle(just_actor_image, (actor_x, actor_y), 3, (1), thickness=-1, lineType=cv2.LINE_AA, shift=0)
        
        # enlarge image by factor of 2
        # big = cv2.resize(zi, (zi.shape[1]*2, zi.shape[0]*2), interpolation=cv2.INTER_CUBIC)
        ret, dark_region = cv2.threshold(zi, 0.5, 1, cv2.THRESH_TOZERO)

        inverted = np.ones(zi.shape, dtype=np.float32) - zi
        ret, dark_region2 = cv2.threshold(inverted, 0.5, 1, cv2.THRESH_TOZERO)

        # return zi
        returning = np.array([just_actor_image*255, dark_region*255, dark_region2*255], dtype=np.uint8).copy()
        return returning

    def drawRect(self, img, z0, z1, color):
        if(len(img.shape) == 2):
            fake = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        else:
            fake = img.copy()
        

        box_width = 120/16
        box_height = 80/12



        actual_start = (int(box_width * z1), int(box_height * z0))
        actual_end = (int(box_width * (z1+1)), int(box_height * (z0+1)))

        cv2.rectangle(fake, actual_start, actual_end, color, thickness=1, lineType=cv2.LINE_AA, shift=0)
        return fake

    def drawSimple(self, frame):

        actor_frame = np.zeros(shape=(80,120), dtype=np.uint8)
        team_frame = np.zeros(shape=(80,120), dtype=np.uint8)
        opp_frame = np.zeros(shape=(80,120), dtype=np.uint8)

        actor_x, actor_y = -1, -1

        for player in frame['freeze_frame']:
            if(player['actor']):
                actor_x = int(player['location'][0])
                actor_y = int(player['location'][1])

                # draw circle at actor_x, actor_y on actor_frame with cv2
                cv2.circle(actor_frame, (actor_x, actor_y), 3, (255,255,255), thickness=-1, lineType=cv2.LINE_AA, shift=0)
            elif(player['teammate']):
                # draw circle at x, y on team_frame with cv2
                cv2.circle(team_frame, (int(player['location'][0]), int(player['location'][1])), 3, (255,255,255), thickness=-1, lineType=cv2.LINE_AA, shift=0)
            elif(not player['teammate']):
                # draw circle at x, y on opp_frame with cv2
                cv2.circle(opp_frame, (int(player['location'][0]), int(player['location'][1])), 3, (255,255,255), thickness=-1, lineType=cv2.LINE_AA, shift=0)




        

        returning = np.array([actor_frame, team_frame, opp_frame], dtype=np.uint8).copy()
        return returning
    # Create a dataset containing images
    # Observation: 
    # Image of player
    # Image of team mates
    # Image of opponents
    # y1: Predicted Action
    # y2: zone 0
    # y3: zone 1
    def createImageDataset(self):
        x = []
        y = []
        rewards = []
        event_ids = []
        terminals = []


        for i in tqdm(range(len(self.events)-2)):

            # if( i > 50 ): break
            self.ratio = 2
            event = self.events[i]
            next_event = self.events[i+1]
            related_event = self.tracking_content[event['id']]

            # from view import Visualiser
            # visualiser = Visualiser()

            # blank_image = np.zeros((visualiser.ratio*visualiser.height, visualiser.ratio*visualiser.width, 3), np.uint8)
            # blank_image[:] = (18, 97, 41)

            # # visualiser.loadContent('data.json')
            # visualiser.loadTrackingContent(r'three-sixty\3788741.json')
            # visualiser.drawAllPlayers(blank_image, None, event['id'])

            # cv2.imshow("all", blank_image)
            
            # print("showed")

            # Get the image
            # returned_img = self.drawIDW(related_event)
            
            # end location
            end_location = [6,8]
            try:
                end_location = event[event['type']['name'].lower()]['end_location']
            except Exception as e:
                pass

            zone = self.get_zone_from_coords(end_location[0], end_location[1])

            img = self.drawSimple(related_event)

            x.append(img)

            event_ids.append(event['id'])


            # Get the action
            chosen_action = int(self.getIDFromAction(event))
            one_hot = self.oneHot(chosen_action)
            one_hot.append(end_location[0]/120)
            one_hot.append(end_location[1]/80)
            # one_hot.append(zone[0]/15)
            # one_hot.append(zone[1]/11)

            y.append(one_hot)

            reward = self.calculate_reward(event, next_event)
            rewards.append(reward)
            terminals.append(0 if reward != -1 else 1)
        
        return np.array(x, dtype=np.uint8), np.array(y), np.array(rewards), np.array(event_ids), np.array(terminals)


    # Dataset specifications:
    # x:
    # float: action ID (0 = PASS, 1 = SHOOT...etc)

    # y:
    # one hot encoded of location
    def createEpisodeDataset(self):

        print("Events length: ", len(self.events))

        x, y, rewards, event_ids = [], [], [], []

        current_actions = []
        lim = self.lim
        possession_team = -1
        for i in range(len(self.events)-1):

            team_id = self.events[i]['possession_team']
            # new possession sequence. save the old one
            if(team_id != possession_team and len(current_actions) >= (lim+1)):
                for_6 = int(len(current_actions)/(lim + 1))
                sequences = np.array_split(np.array(current_actions), for_6)
                for sequence in sequences:
                    seq_x = [[self.getIDFromAction(item), self.get_XT_Zone(item)[0], self.get_XT_Zone(item)[1]] for item in sequence[:lim]]
                    seq_y = self.getIDFromAction(sequence[-1])
                    

                    # from view import Visualiser 
                    # visualiser = Visualiser()

                    # a = False
                    first_5_zipped = zip(sequence, sequence[1:])
                    # for e in sequence:
                    #     if e['type']['name'] == 'Shot': a = True
                    seq_r = [self.calculate_reward(current_event, next_event) for current_event, next_event in first_5_zipped]

                    # if a and i== 391:
                    #     for i2, ev in enumerate(sequence):



                    #         # print(len(sequence), sequence[0]['id'], sequence[0]['id'] in self.tracking_content)
                    #         players_per_zone, oppo_players_per_zone = self.getPlayersPerZone(self.tracking_content[ev['id']])
                    #         visualiser.drawIDW(self.tracking_content[ev['id']])

                    #         image = visualiser.draw_single_frame(ev['location'], self.tracking_content[ev['id']])
                    #         # cv2.imshow("simple_players", image)
                    #         image = visualiser.show_players(image, players_per_zone, oppo_players_per_zone)
                    #         # cv2.imshow("grid", image)

                    #         radii = [25, 65, 140]
                    #         team_per_radius, oppo_per_radius = self.getPlayersPerRadius(self.tracking_content[ev['id']], ev['location'], radii)
                    #         image  = visualiser.draw_players_per_circle(image, ev['location'], radii, team_per_radius, oppo_per_radius)
                    #         # cv2.imshow("radii", image)
                            

                    #         areas = cv2.imread("myfig.png")
                    #         # print(image.shape)
                    #         resized = cv2.resize(areas, (image.shape[1], image.shape[0]),  cv2.INTER_AREA)

                    #         # cv2.imshow("areas", resized)

                    #         image = visualiser.draw_single_frame(ev['location'], self.tracking_content[ev['id']])

                    #         alpha = 0.4
                    #         image = cv2.addWeighted(image, alpha, resized, 1 - alpha, 0)
                    #         image = visualiser.show_players(image, players_per_zone, oppo_players_per_zone)
                    #         image = visualiser.draw_single_frame(ev['location'], self.tracking_content[ev['id']])


                    #         # cv2.imshow("superimposed " + str(i), image)
                    #         cv2.imwrite("tmp/"+str(i)+"-"+str(i2)+".png", image)
                    #         try:
                    #             print(ev['type'], seq_r[i2])
                    #         except:
                    #             print(ev['type'], ev['shot']['statsbomb_xg'])

                    #         # cv2.waitKey(0)
                    #         cv2.destroyAllWindows()
                    #     print(sequence[-1]['shot']['statsbomb_xg'])
                    #     print("-" * 20)
                    #     # exit()
                    event_ids.append([item['id'] for item in sequence])


                    x.append(np.array(seq_x).flatten())
                    y.append(seq_y)
                    rewards.append(seq_r[0])
                    
                current_actions = []
            else:
                current_actions.append(self.events[i])


        
        return np.array(x), np.array(y), np.array(rewards), np.array(event_ids)
            
    # Dataset specifications:
    # x:
    # float: action ID (0 = PASS, 1 = SHOOT...etc)
    # float: x coordinate of action
    # float: y coordinate of action

    # y1:
    # one hot encoded vector of next location
    # y2:
    # x value of next location
    # y3:
    # y value of next location

    def loadTrackingContent(self, path):
        with open(path, 'r') as file:
            raw_tracking = json.loads(file.read())

        game_id = path.split("\\")[-1][:-5]
        self.games_with_tracking[game_id] = 0

        for item in raw_tracking:
            self.tracking_content[item['event_uuid']] = item

    def loadTrackingContentFromDir(self, dir):
        files = glob.glob(dir)
        print("Loading tracking content:")
        for _file in tqdm(files[:self.file_limit]):
            self.loadTrackingContent(_file)

    def createDatasetMultY(self):

        x, y1, y2, y3 = [], [], [], []
        for i in range(len(self.events)-1):

            action = self.events[i]
            next_action = self.events[i+1]

            x_entry = [self.getIDFromAction(action), action['location'][0], action['location'][1]]
            y_class = np.zeros((len(self.good_events)))
            y_class[int(self.getIDFromAction(next_action))] = 1
            
            

            y_pos = self.getEndLocationFromAction(next_action)
            if(y_pos is None): continue
            
            x.append(x_entry)
            y1.append(y_class)
            y2.append(y_pos[0]/120)
            y3.append(y_pos[1]/80)

        return np.array(x), np.array(y1), np.array(y2), np.array(y3)


    def getActionFromID(self, id_):
        return self.events[self.ids[id_]] if id_ in self.ids else None

    # Dataset specifications:
    # x:    2D Array
    #       One hot encoded action. 5 actions

    # y:    Next Action
    def createDataset(self):

        x, y = [], []
        for i in range(len(self.events)-1):

            action = self.events[i]
            next_action = self.events[i+1]

            x_entry = [self.getIDFromAction(action), action['location'][0], action['location'][1]]
            y_entry = np.zeros((len(self.good_events)))
            y_entry[int(self.getIDFromAction(next_action))] = 1
            
            x.append(x_entry)
            y.append(y_entry)

        return np.array(x), np.array(y)

    def oneHot(self, chosenAction):
        empty = [0 for i in range(len(self.good_events))]
        empty[chosenAction] = 1

        return empty

    def getEndLocationFromAction(self, action):
        try:
            action_type = self.getIDFromAction(action)
            if(action_type == self.SHOOT): return action['location']
            if(action_type == self.PASS): return action['pass']['end_location']
            if(action_type == self.CARRY): return action['carry']['end_location']
        except Exception as e:
            print("Failed:", e)
            return None

    def loadFile(self, file_location):
        
        with open(file_location, 'r', encoding='utf-8') as file:
            game = json.load(file)

        if(self.events is None):
            self.events = []

        filtered_game = self.filter_game(game)

        for event in filtered_game:
            if event['id'] in self.tracking_content:
                self.ids[event['id']] = len(self.events)
                self.events.append(event)

    def loadFilesFromDir(self, dir, filterGamesWithoutTrackingData=False):
        files = glob.glob(dir)
        files_loaded = 0
        lim = self.file_limit if not filterGamesWithoutTrackingData else -1

        file_progress = tqdm(files[:lim])
        for file_ in file_progress:

            game_id = file_.split("\\")[-1][:-5]
            if (filterGamesWithoutTrackingData and game_id in self.games_with_tracking):

                if((self.events is not None) and self.file_limit != -1 and files_loaded > self.file_limit):
                    return

                self.loadFile(file_)
                file_progress.set_description("file count: " + str(files_loaded) + " / " +str(self.file_limit)) 
                
                
                files_loaded += 1
            elif(not filterGamesWithoutTrackingData):
                self.loadFile(file_)
    
    def loadFilesFromDirFake(self, dir):
        files = glob.glob(dir)
        counter_has = 0
        counter_doesnt = 0

        for file_ in tqdm(files[:self.file_limit]):

            game_id = file_.split("\\")[-1][:-5]
            if game_id in self.games_with_tracking:
                counter_has += 1
            else:
                counter_doesnt += 1

        return counter_has, counter_doesnt

    def saveFiles(self, file_name):
        np.save("np_db/" +file_name, np.array(self.events))

    def leadFiles(self, file_name):
        self.events = np.load("np_db/" +file_name) # load
def main():
    datasetMaker = CreateDataset()

    # x, y1, y2 = datasetMaker.createDatasetMultY()

    # datasetMaker.loadTrackingContent('data_track.json')
    
    # counter_has, counter_doesnt = datasetMaker.loadFilesFromDirFake('events/*.json')
    # print(counter_has, counter_doesnt)
    # datasetMaker.filterByGamesWithTrackingData()
    # datasetMaker.loadFile('data.json')
    # datasetMaker.getRelated


    # datasetMaker.loadTrackingContent('data_track.json')
    datasetMaker.loadTrackingContentFromDir('three-sixty/*.json')
    datasetMaker.loadFilesFromDir('events/*.json', filterGamesWithoutTrackingData=True)
    print("Tracking Content", len(datasetMaker.tracking_content))
    print("Filtered Events then...", len(datasetMaker.events))
    x, y, rewards, event_ids = datasetMaker.createEpisodeDataset()


    
    print("Shape")
    print(x.shape, len(x))
    # print(datasetMaker.getPlayerFromActionID(event_ids[0]))


    
    # print(x[0], y[0], rewards[0])


    # print(datasetMaker.xT_Map.shape)
    # map_0 = {}
    # map_1 = {}
    # for i in range(120):
    #     # for j in range(80):
    #     z0, z1 = datasetMaker.get_zone_from_coords(i,0)

    #     if z1 in map_1 and not (i in map_1[z1]): map_1[z1].append(i)
    #     elif not (z1 in map_1): map_1[z1] = [i]
            
    #         # if z1 in map_1 and not (j in map_1[z1]): map_1[z1].append(j)
    #         # elif not (z1 in map_1): map_1[z1] = [j]

    # with open ("test.json", "w") as file:
    #     json.dump(map_0, file)

    # print(x.shape, y.shape, rewards.shape)

def main2():
    datasetMaker = CreateDataset()
    datasetMaker.file_limit = -1
    datasetMaker.loadTrackingContentFromDir('three-sixty/*.json')
    datasetMaker.loadFilesFromDir('events/*.json', filterGamesWithoutTrackingData=True)
    x, y, z, b, c = datasetMaker.createImageDataset()

    tmp_file = TemporaryFile()
    arr_1 = np.arange(10)
    arr_2 = np.arange(10)
    np.savez("saved_datasets\\testing.npz", x, y, z, b, c)

    print(x.shape)

if __name__ == "__main__":
    # main()
    main2()