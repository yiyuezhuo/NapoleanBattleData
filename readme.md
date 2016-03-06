# The basic analysis to data from Napolean war battle

## Data location

Data was saved in NaD3.xlsx .

## About Data

Following sections is copyed from the post from "Chinese Napolean forum ".

http://bbs.napolun.com/forum.php?mod=viewthread&tid=38675&highlight=

This projects collect and clean up summary part by 200+ wikipedia pages in Napoleonic Wars category.The core is extracting the quantization information.If you are interested in empirical research,you would to look it for fun. Most of the pages are mapped to a record of table. There records to contain variables as name,backend(eg. peninsula war),location,result,commander,strengths,strength losses etc.

I run a Python crawler to scratch these pages and extract data by bs4.BeautifulSoup. Aften that, I hand tag who victory is and merge "big victory","small victory"etc to a single "victory" class. However,some battle strength is recorded by range format,I map these to its mean,if a battle is related to many fields,I will aggregation them.If presence numbers and engaged number is different,I take engaged numbers.So the data is unique ,this lead it can be empirical analyzed.

* It only included battles between 1805 and 1815.
* Its type includes sea,siege,land.Please notice the difference if you found a strange number.
* If a table is farther right for another, then the table is processing more than another except table Exam.

My motivation to do this project is two papers below:

* [1] Ruobing Liang. Climate impact and the religious cases in the End of Qing Dynasty [J]. Economics (Quarterlu),2014,04:1557-1584.
* [2] Qiang Chen Climate impact,Dynasty period and the conquest of nomadic people. [J]. Economics (Quarterlu),2015,01:373-394.

However, battle data is more complex than their object of study, as battle data lack the effect of aggregation. Selecting a regress model is hard and every time soldiers fighting capacity are not homogeneity.For example,I sum the Spain strength and Britsh strength into allies strength factors of Penisula War. While it made some sense, but I feel it is not matching my ideal object of study (eg. commander ability).

## A simple analysis

I estaablish the logistic model in 157 battles filtered from all battles. The dependent variables is dummy variable that is 1 if allies is victory 0 if french is victory.Independent variables include StrengthF(the strength of French),StrengthA(the strength of allies),Napolean,MichelNey,JoachimMurat,WW(dummy variable,if his name appears in wiki summary commander items is 1 else 0. WW represents Wellington/Wellesley). This model got a 65% accuracy,it's poor,but it's only a simple example.

regress summary


                          B        S.E,        Wals          df         Sig.      Exp (B)
        StrengthF        .000        .000        2.880        1        .090        1.000
        StrengthA        .000        .000        7.202        1        .007        1.000
        Napolean       -1.937        .689        7.892        1        .005        .144
        MichelNey      -1.550        .747        4.302        1        .038        .212
        JoachimMurat     .950        .606        2.456        1        .117        2.586
        WW              2.276        .734        9.608        1        .002        9.736
        Constant        -.257        .267        .923         1        .337        .774


The estimated regression coefficient in logistic models has not an explicit explain as ordinary linear model. You can see relevant books for details. But in this case, I will show some special scenes to show the effect of these independent variables. The baseline scene is 50000 French vs 50000 allies without commander dummy variables.

Q is predict probability of allies victory by model.
P is sig indicator in the table above.

### Special case predict and explain

* 50000 French VS 50000 Allies Q=46% (This imply the French fighting capacity is more than Allies)
* 75000 French VS 50000 Allies 30%
* 50000 French VS 75000 Allies 64%
* 50000 French + Napolean VS 50000 Allies 11% (Napolean's bonus is significance!)
* 50000 French + Ney VS 50000 Allies 15 % (P=0.038 it is reject null hypothesis for alpha=0.05 )
* 50000 French + Murat VS 50000 Allies 68% (However, Murat bonus is negetive ,though it is not significance.)
* 50000 French VS 50000 Allies + Wellington 89% (Wellington's bonus is significance too.)
* 50000 French VS 50000 Allies + Wellington 63% (Wellington 's ability is more than Ney.It also can be seen in regression coefficient.)

Why Murat'bonus is negative? Because he is loss so many battles over 1815. This bad record pulled down the score model to assign to him by likelihood function used by model. The negative and positive is compare to "mean effect" baseline."mean effect" means ,for example, Blucher,Davout and other unconsidered commander's mean effect.Murat is bad at them mean ability.It has some fitfall,because you can't identify the effect of Murat not as a main commander (so he didn't appear the wiki commander item) in the field. 

# 拿破仑战争战役数据及粗略分析

## 数据

处理过的数据放在NaD3.xlsx里

## 例子

以下内容直接复制自以前在中文拿破仑论坛发表的帖子

http://bbs.napolun.com/forum.php?mod=viewthread&tid=38675&highlight=

收集并整理了wiki下Napoleonic Wars类别下200多个战役的summary。主要是提取其中的量化信息，对计量实证感兴趣的可以看看。大多数战役都有其名称，背景（半岛战争这种），位置，结果，指挥官，参战双方兵力，参战双方兵力损失等。数据抓取是直接用python写爬虫爬了那些词条并用bs4提取的信息。之后我自己又把数据折腾了一下，给多数战役都明确指定了到底谁赢，抛弃了大胜小胜战略胜利战术失败之类的区别。人数等如果出现区间，就计算均值，如果出现多个战区，就加总，如果有在场和实际参战数量的差别，就取实际参战数量。这样这些数据就可以直接进行计量分析了，虽然有没有意义另说。

* N1 这里只包含了1805及之后的战役
* N2 这里包含海战，攻城战和陆战，注意区分。
* N3 各个表中除了Exam都是从左往右加工越来越多的。

不知道诸位对计量史学有何了解，我是看了这两篇论文才想起找数据弄弄但找不到才收集的。

* [1]梁若冰. 气候冲击与晚清教案[J]. 经济学(季刊),2014,04:1557-1584.
* [2]陈强. 气候冲击、王朝周期与游牧民族的征服[J]. 经济学(季刊),2015,01:373-394.

不过战争的数据相比他们研究的对象复杂得多，比如直接上回归的话模型不好选择，而且各个时期的兵力也不是相同的，乃至像半岛战争我是把西班牙兵力与英军兵力直接求和算联军兵力的话，虽然这样算也有相应的统计意义，但总觉得与所想研究的对象（如将领能力等）相差甚远。

抛砖引玉，先作一些粗略的计量分析。完全不管什么内生性之类的问题，因为细究的话模型就肯定是不对的。

筛选出157个战役进行logistic回归，因变量为法军胜利（取0）或是联军胜利（取1）。自变量有法军兵力数，联军兵力数与拿破仑，内伊，缪拉，威灵顿是否作为主要指挥官（wiki里commander是否有他名字）作为虚拟变量。可以将54%的预测准确度升到65%，不算好，不过这只是例子。

回归的系数结果

                          B        S.E,        Wals          df         Sig.      Exp (B)
        StrengthF        .000        .000        2.880        1        .090        1.000
        StrengthA        .000        .000        7.202        1        .007        1.000
        Napolean       -1.937        .689        7.892        1        .005        .144
        MichelNey      -1.550        .747        4.302        1        .038        .212
        JoachimMurat     .950        .606        2.456        1        .117        2.586
        WW              2.276        .734        9.608        1        .002        9.736
        常量            -.257        .267        .923         1        .337        .774

logistic回归的系数不想线性回归那样好解释。具体含义可以去看相关资料。这里我给出一些例子来比较。以50000法军兵力对阵50000联军兵力的预测概率为标准，比较各种情况。

下面的概率可以看成联军胜率Q，或者1-Q就得到了法军胜率。（下文的P是指上面那个表的sig值，显著性水平，这个值粗略地说可以看成其对模型影响为0的概率，所以对于其存在感该值越低越好）

50000法军 VS 50000联军 46% （这说明平均法军战力比联军强）

75000法军 VS 50000联军 30%

50000法军 VS 75000联军 64%

50000法军+拿破仑 VS 50000联军 11% (拿破仑的加成是统计显著地)

50000法军+内伊 VS 50000联军 15% （P=0.038,5%水平下显著）

50000法军+缪拉 VS 50000联军 68% （缪拉实际上是提供减成。。恩，不过P=0.11不显著）

50000法军 VS 50000联军+威灵顿 89% (铁公爵的加成也是显著的)

50000法军+内伊 VS 50000联军+威灵顿 63% (威灵顿还是比内伊强，当然这个看回归系数就看出来了)

为什么缪拉是提供减成的呢？因为其在1815战役里多数战役都失败了，由于其成功跻身wiki主要指挥官的多数战役里怒刷战绩，所以从似然性角度来看，似乎把他看成减战力的比把他看成加战力的要更有可能。这个减与增是相对的，可能有人觉得无论如何有他总比没他好，这个某种意义上是对的，可以通过改变似然函数来实现这个效果。不过也要注意这些回归里截距和误差项提供了一个参考基线，也就是说在某些没有捕捉到的变量里（比如布吕歇尔就没有作为虚拟变量加入），缪拉与这些效应的平均水平相比，可能要更差一些。毕竟的确其作为主要指挥官的“大多数”战役都失败了，假如根据规模加权可能会好一点。可是无论如何，要是用回归的眼光来看，马谡这类的肯定是提供减成的。。因为没有他出场但胜利了的变异来扳回一城。
