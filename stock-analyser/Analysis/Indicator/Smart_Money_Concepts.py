import pandas
from talib import abstract


def smart_money_concepts(dataframe,length,ifilter_confluence =False):
    df = pandas.DataFrame()
    atr = abstract.ATR(dataframe,200).to_frame()
    atr.rename(columns={0: 'atr'}, inplace=True)
    upper = dataframe['high'].rolling(length).max()
    lower = dataframe['low'].rolling(length).min()
    upper_i = dataframe['high'].rolling(5).max()
    lower_i = dataframe['low'].rolling(5).min()
    df['upper'] =upper
    df['lower'] = lower
    df['upper_i'] = upper_i
    df['lower_i'] = lower_i
    df['high_len'] =dataframe['high'].shift(length)
    df['low_len'] = dataframe['low'].shift(length)
    df['high_i'] = dataframe['high'].shift(5)
    df['low_i'] = dataframe['low'].shift(5)
    df['high'] = dataframe['high']
    df['open'] =dataframe['open']
    df['close'] = dataframe['close']
    df['low'] =dataframe['low']
    # default atr and cmean_range not do..
    df['ob_threshold'] = atr

    data_cache=[]



    #filtering
    bull_concordant = [True]
    bear_concordant = [True]
    #swings
    oswl = [0]
    top = []
    btm = []
    oswli = [0]
    itop = []
    ibtm = []

    top_y = [0]
    top_x = [0]
    btm_y = [0]
    btm_x = [0]
    itrend = [0]
    itop_y = [0]
    itop_x = [0]
    ibtm_y = [0]
    ibtm_x = [0]
    itop_cross = [True]
    ibtm_cross = [True]

    #BOH CHOCH
    bull_boh_choch=['None']
    bear_boh_choch = ['None']
    #ob block

    ob_block=[]


    i = 0
    for data in df.itertuples():
        osw =0
        oswi = 0

        if len(data_cache) > length+1:
            data_cache.pop(0)
        data_cache.append(data)

        if data[5] > data[1]:
            osw = 0
        elif data[6] < data[2]:
            osw = 1
        else:
            osw =oswl[-1]

        if data[7] > data[3]:
            oswi = 0
        elif data[8] < data[4]:
            oswi = 1
        else:
            oswi = oswli[-1]

        if len(oswl) > 1:
            oswl.pop(0)
        oswl.append(osw)

        if len(oswli) >1:
            oswli.pop(0)
        oswli.append(oswi)

        if len(oswl) <=1 or len(oswli) <=1:
            continue
        if oswl[-1] == 0 and oswl[-2] !=0:
            top.append(data[5])
        else:
            top.append(0)
        if oswl[-1] ==1 and oswl[-2] !=1:
            btm.append(data[6])
        else:
            btm.append(0)

        if oswli[-1] == 0 and oswli[-2] !=0:
            itop.append(data[7])
        else:
            itop.append(0)
        if oswli[-1] ==1 and oswli[-2] !=1:
            ibtm.append(data[8])
        else:
            ibtm.append(0)

        #pivot high
        if top[-1]:
            if i > 0:
                top_y.append(top[-1])
                top_x.append(i-length)
            else:
                top_y[0] = top[-1]
                top_x[0] = i-length
        else:
            if i > 0:
                top_y.append(top_y[-1])
                top_x.append(top_x[-1])

        if itop[-1] :
            if i > 0:
                itop_cross.append(True)
                itop_y.append(itop[-1])
                itop_x.append(i-5)
            else:
                itop_cross[0] = True
                itop_y[0] = itop[-1]
                itop_x[0] = i-5
        else:
            if i > 0:
                itop_cross.append(itop_cross[-1])
                itop_y.append(itop_y[-1])
                itop_x.append(itop_x[-1])

        # pivot low
        if btm[-1]:
            if i > 0:
                btm_y.append(btm[-1])
                btm_x.append(i-length)
            else:
                btm_y[0] = btm[-1]
                btm_x[0] = i-length
        else:
            if i > 0:
                btm_y.append(btm_y[-1])
                btm_x.append(btm_x[-1])

        if ibtm[-1] :
            if i > 0:
                ibtm_cross.append(True)
                ibtm_y.append(ibtm[-1])
                ibtm_x.append(i-5)
            else:
                ibtm_cross[0] = True
                ibtm_y[0] = ibtm[-1]
                ibtm_x[0] = i-5
        else:
            if i > 0:
                ibtm_cross.append(ibtm_cross[-1])
                ibtm_y.append(ibtm_y[-1])
                ibtm_x.append(ibtm_x[-1])

        if i > 0:
            itrend.append(0)

        #Pivot High BOS/CHoCH
        block_dict = {}
        if ifilter_confluence:
            if i == 0:
                bull_concordant[0] = data[9] - max(data[11],data[10]) >min(data[11],data[10]-data[12])
            else:
                bull_concordant.append( data[9] - max(data[11], data[10]) > min(data[11], data[10] - data[12]))
        cross_over = False
        if len(data_cache) >1 and data_cache[-1][11] > itop_y[-1] and data_cache[-2][11] <= itop_y[-2]:
            cross_over = True
        #if cross_over and itop_cross[-1] and top_y[-1] != itop_y[-1] and bull_concordant[-1]:
        if cross_over and itop_cross[-1] and bull_concordant[-1]:
            min_value = 99999999.
            max_value = 0.
            idx = 1

            choch = False
            if itrend[-1] < 0:
               choch = True
            if i > 0:
                bull_boh_choch.append('CHoCH' if choch else 'BOS')
            else:
                bull_boh_choch[0] = 'CHoCH' if choch else 'BOS'
            itop_cross[-1] = False
            itrend[-1] = 1
            tx = i - itop_x[-1]+1
            if tx > 1:
                for j in range(2, tx):
                    if data_cache[-j][9] - data_cache[-j][12] < data_cache[-j][13] * 2:
                        min_value = min(data_cache[-j][12], min_value)
                        if min_value == data_cache[-j][12]:
                            max_value = data_cache[-j][9]
                            idx = j
            #ob_coord(false, itop_x, iob_top, iob_btm, iob_left, iob_type)
            block_dict['iob_top'] = max_value
            block_dict['iob_btm'] = min_value
            block_dict['iob_left'] = data_cache[-idx][0]
            block_dict['iob_type'] = 1
            ob_block.append(block_dict)
        else:
            bull_boh_choch.append('None')


        #/Pivot Low BOS/CHoCH
        if ifilter_confluence:
            if i == 0:
                bear_concordant[0] = data[9] - max(data[11], data[10]) < min(data[11], data[10] - data[12])
            else:
                bear_concordant.append(data[9] - max(data[11], data[10]) < min(data[11], data[10] - data[12]))
        cross_under = False
        if len(data_cache) > 1 and data_cache[-1][11] < ibtm_y[-1] and data_cache[-2][11] >= ibtm_y[-2]:
            cross_under = True
        #if cross_under and ibtm_cross[-1] and btm_y[-1] != ibtm_y[-1] and bear_concordant[-1]:
        if cross_under and ibtm_cross[-1]  and bear_concordant[-1]:
            min_value = 99999999.
            max_value = 0.
            idx = 2

            choch = False
            if itrend[-1] > 0:
                choch = True
            if i > 0:
                bear_boh_choch.append('CHoCH' if choch else 'BOS')
            else:
                bear_boh_choch[0] = 'CHoCH' if choch else 'BOS'
            ibtm_cross[-1] = False
            itrend[-1] = -1
            tx = i - ibtm_x[-1]+1
            if tx > 1:
                for j in range(2, tx):
                    if data_cache[-j][9] - data_cache[-j][12] < data_cache[-j][13] * 2:
                        max_value = max(data_cache[-j][9], max_value)
                        if max_value == data_cache[-j][9]:
                            min_value = data_cache[-j][12]
                            idx = j
            # ob_coord(true, ibtm_x, iob_top, iob_btm, iob_left, iob_type)
            block_dict['iob_top'] = max_value
            block_dict['iob_btm'] = min_value
            block_dict['iob_left'] = data_cache[-idx][0]
            block_dict['iob_type'] = -1
            ob_block.append(block_dict)
        else:
            bear_boh_choch.append('None')

        #order block filter
        k = 0
        while k < len(ob_block):
            if data[11] < ob_block[k]['iob_btm'] and ob_block[k]['iob_type'] ==1:
               ob_block.pop(k)
            elif data[11] > ob_block[k]['iob_top'] and ob_block[k]['iob_type'] ==-1:
                ob_block.pop(k)
            else:
                k +=1
        i += 1




    return ob_block










