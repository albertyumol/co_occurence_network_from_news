import numpy as np
import pandas as pd
import streamlit as st
import bokeh
from datetime import date, timedelta
from numpy import interp
from PIL import Image
import pydeck as pdk
from collections import defaultdict

import networkx as nx

# from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral11, Category20c, viridis, Spectral6
from bokeh.transform import linear_cmap
from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges
from networkx.algorithms import community
from bokeh.transform import factor_cmap
import itertools

# st.set_page_config(layout="wide")
st.title('Co-Occurence Network PH Elections 2022')


image = Image.open('omdena_logo.png')
st.sidebar.image(image, caption='', use_column_width=True)


def co_occurrence(sentences, window_size):
    d = defaultdict(int)
    vocab = set()
    for text in sentences:
        # preprocessing (use tokenizer instead)
        text = text.lower().split()
        # iterate over sentences
        for i in range(len(text)):
            token = text[i]
            vocab.add(token)  # add to vocab
            next_token = text[i+1 : i+1+window_size]
            for t in next_token:
                key = tuple( sorted([t, token]) )
                d[key] += 1

    # formulate the dictionary into dataframe
    vocab = sorted(vocab) # sort vocab
    df = pd.DataFrame(data=np.zeros((len(vocab), len(vocab)), dtype=np.int16),
                      index=vocab,
                      columns=vocab)
    for key, value in d.items():
        df.at[key[0], key[1]] = value
        df.at[key[1], key[0]] = value
    return df




add_selectbox = st.sidebar.radio(
    "",
    ("Context", "Data Set", "Methodology",
     "Exploratory Data Analysis",
     "Network Analysis", "References","Author")
)

if add_selectbox == 'Context':
    st.subheader('Problem Statement')
    st.write('-----------------------------------------------------------------------')
    st.write('Mention frequency with span window of 30.')



elif add_selectbox == 'Network Analysis':
    text_init = ["With President Duterte s calling him a weak leader still fresh, Bongbong Marcos avoids talking about details of the drug war. Presidential aspirant Ferdinand Bongbong Marcos Jr is bent on wooing the Duterte vote, saluting President Rodrigo Duterte s leadership at a speech before local officials in Cebu City. Disregarding a rebuke by Duterte, calling Marcos a weak leader and a spoiled child, the son of deposed dictator said on Friday, November 26, that the presidents brand of leadership must be continued to beat the pandemic. Pagkatapos ng pagka-lider ng ating Pangulo, ang Pangulong Rodrigo Duterte, ay kailangan pa rin na matibay ang leadership dahil nandito pa rin ang problema, Marcos said on Friday during the regional meet of the League of Municipalities of the Philippines (LMP), the president of which is his ally, Narvacan, Ilocos Sur mayor Chavit Singson. (After the leadership of our president, President Rodrigo Duterte, we still need strong leadership because the problem is still here.) Earlier, Marcos spokesperson Vic Rodriguez said that We respect the president at hindi nagbabago yung pag galang, respeto, at mataas na pagkilala at pagtingin sa kaniya ni Bongbong Marcos. (We respect the president and Bongbong Marcos respect and highest recogniton for him has not changed.) This was after a series tirades from Duterte, from accusing Marcos of orchestrating that his daughter Sara run for vice president instead of president, to calling him a weak leader. In the same speech Duterte throws a blind item against a cocaine-using candidate. Sara, who doesnt shy away from public quarrels with his father, has not addressed Duterte s remarks but has instead been hyping Marcos in her speeches, speaking highly of his running mates experience in government. Hanas na siya sa decision-making (He s used to decision-making), said Sara of Marcos in an earlier event Friday in Misamis Occidental before following in Cebu at the LMP meet. It is apparently addressed to the theme of his critics that he has little to show for his over 20 years in government. A divisive figure because of his fathers dictatorial rule marked with human rights violations and corruption, Marcos has so far stuck to a message of unification and says he shuns gutter politics. And there s no better unification message than combining his North and Sara s South. The North and the South have come together. Totoo nga naman yun dahil kami ay galing sa Norte at si Inday Sara naman ay galing Mindanao. Talagang may ibig sabihin ang aming pagsasama dahil ipinagsasama namin ang buong Pilipinas, said Marcos. (That s true because were from the North and Inday Sara is from Mindanao. Our alliance really is symblic because by coming together, we are unifying the country.) Before she filed her candidacy for vice president, Sara – who was being pushed to run for president – topped the September Pulse Asia presidential preference survey in Mindanao voters (47%) and Visayas (23%). Marcos won Northern Luzon in the 2016 elections, but he lost Cebu to Vice President Leni Robredo. It s the second time that Marcos went to Cebu City with Sara. Backing of 44 mayors So far, the alliance with Sara has bore fruit. On Friday night, Sara s spokesperson, Liloan Mayor Christina Frasco, chair of LMP-Cebu, said 44 mayors have agreed to back Marcos. On behalf of all the 44 mayors of the province of Cebu, particular to the mayors of the 5th district, as well as my fellow mayors in the Visayas, for whom I am the national vice president, we hereby express our unequivocal support to you, for your candidacy and we will do everything in our power to ensure an unequivocal victory in the coming elections, said Frasco. The Marcos-Sara tandem has secured the support of Partido ng Masang Pilipino (PMP) of former president and Manila mayor Joseph Erap Estrada. Sara is running under Lakas-CMD, the party of former president Gloria Macapagal-Arroyo. Senator Bong Go, Duterte s chosen one and the standard-bearer of the ruling party, may be entertaining thoughts of withdrawing from the presidential race, according to politicians who attended a dinner with Go and the president. While Dutertes blind item against a cocaine-using presidential candidate has put Marcos in negative light because of the presidents clue that the candidate has a prominent father, it has also put the drug war in question.",

"Presidential aspirant and Manila Mayor Francisco Isko Moreno Domagoso on Friday, said he was committed to creating a medium and long-term plan and fund to boost the country s agricultural sector if he wins the upcoming election. High time naman na yung mga ahensya ng gobyerno makapagplano ng dire-diretso because ang funding nila garantisado. Its a five-year plan and 10-year plan. Di tayo year on year lang magpaplano (It is high time that government agencies to plan directly because their funding is guaranteed. It s a five-year plan and 10-year plan. We should not just plan year on year), he said during the Halalan 2022 Para sa Agrikultura dialogue at the Manila City Hall on Friday. Magkakaroon ng kapantagan yung mga magsasaka at yung mga mangingisda sa industriya ng agrikultura in the next 5 years or in the next 10 years. Ito yung pupuntahan kong journey. Di na siya aasa na every year, hihingi ng pondo o maglolobby ng pondo (Farmers and fishermen will gain a certainty in the agricultural industry in the next fiver years or in the next 10 years. This is the journey I am going on. He will no longer expect that every year, he will ask for funds or lobby for funds), he added. Through this, Domagoso believes it will also draw in investors in the agricultural sector. If it s certain, investors will come it. We need investors in agriculture, he said. The Manila mayor also reiterated that the national government should prioritize food security, especially during this time of pandemic. I think this pandemic taught us a very good lesson on how we should give much attention to food security. And it s high time for us na magising ang liderato ng mga ahensya ng gobyerno na pagtuunan ito ng pansin (wake up the leadership of government agencies to focus on it), he said. Also present during the dialogue were Alyansa Agrikultura Chair Ernesto Ordoñez, Federation of Free Farmers Chair Leonardo Montemayor, Chamber of Agriculture and Food President Danilo Fausto, Coalition for Agriculture Modernization in the Philippines Chair Emil Javier, and Bayan sa Agricultura Coordinator Hazel Tanchuling.",

"Parties backed by the country’s biggest political clans will be working towards a Marcos-Sara Duterte win in 2022 Inside Davao – not the city, but a function room in the posh Sofitel Philippine Plaza Manila – the children of two controversial Philippine presidents formalized their 2022 alliance, backed by parties that count former presidents and fellow presidential children as their stalwarts. Lakas-CMD, Partido Federal ng Pilipinas (PFP), Pwersa ng Masang Pilipino (PMP), and Hugpong ng Pagbabago (HNP) signed a four-party alliance agreement on Thursday, November 25. Based on the documents they signed, the four parties will be backing PFP standard-bearer Bongbong Marcos Jr., son of the late dictator Ferdinand Marcos; and Lakas-CMD vice presidential candidate Sara Duterte, the eldest daughter of President Rodrigo Duterte. The top officials of the parties were present at the signing – South Cotabato Governor Reynaldo Tamayo, PFP president; Davao Occidental Governor Claude Bautista, HNP president; Majority Leader Martin Romualdez, Lakas-CMD president; and sormer senator Jinggoy Estrada, PMP president. Explaining their decision to coalesce with each other, Romualdez, Marcos’ cousin, said Lakas-CMD had “vowed to help elect new leaders who will guide and steer us to the right direction.” “We need leaders who have displayed steely nerves in leadership. We need leaders who have solid background in public service. We need leaders with a clear vision on how to keep Filipino families safe and the Philippine economy growing and expanding,” he said. The names in the coalition are anything but new. Lakas-CMD has produced two presidents – Fidel Ramos and Gloria Macapagal Arroyo its president emeritus. PMP is the party of ousted president Joseph Estrada father of current party president Jinggoy.",

"We owe it to our supporters really to do as best we can and fight until the very end, says VP aspirant Senator Kiko Pangilinan Vice presidential aspirant Senator Kiko Pangilinan said there will be no substitutions in his 2022 tandem with Vice President Leni Robredo Pangilinan said this at the Kapihan sa Manila Bay on Wednesday, November 10, where he was asked if he would be open to withdrawing his candidacy to make way for another running mate for Robredo “In terms of itong mga substitution? Wala, wala na ‘yon. Inumpisahan na natin ‘to, and we can see the massive outpouring of support,” Pangilinan said.(In terms of all these substitutions? No, that won’t happen.  We already started this, and we can see the massive outpouring of support.) “We owe it to our supporters really to do as best we can and fight until the very end para maipanalo ang kandidatura ng Ka-TRoPa (to win the candidacy of Ka-TRoPa),” added Pangilinan, who was a reluctant vice presidential candidate. “Ka-TRoPa” – taken from “tropa” or a group of friends – combines the first syllables of the names of Robredo and Pangilinan. He was also asked about the withdrawal of Davao City Mayor Sara Duterte from her citys mayoral race, fueling speculations she would seek a national post. Pangilinan said they had expected Sara Dutertes move, noting it was the same political strategy employed by her father President Rodrigo Duterte in the 2016 polls. Then-mayor Rodrigo Duterte had filed his candidacy for reelection in October 2015 but withdrew it over a month later to substitute for standard-bearer of PDP Laban in 2016. Expected na yan. Ginawa na nila ‘yan nung 2016 ‘yung sinasabing substitution. Inuulit lang nila ‘yung script, ika nga, so it’s no longer a surprise,” the senator said. (We expected that. They already did that kind of substitution in 2016. They are just repeating the script, so it’s no longer a surprise.) He reiterated this during a visit to Batangas with Robredo. I expected this, and now that its happening. Basta kami tuloy-tuloy lang sa aming kampanya, sa pag-iikot. Sa pag-iikot, sa pagko-consolidate ng ating mga supporters. (In our case, we will just continue going around the country and consolidating our supporters.) Electoral aspirants for next year’s elections have until November 15 to file for substitution.",

"Now, if you are in the ICU, who will you choose for a doctor? says Senate President Vicente Sotto III on Rappler's election program On the Campaign Trail Senate President Vicente Sotto III, who is running for vice president as part of a ticket that describes itself as neither pro-opposition or anti-administration, said in an interview that the Philippines was in a crisis, and compared the country to a patient in an intensive care unit (ICU). Yes, nasa ICU tayo. Pandemic, utang, Mandanas ruling na hindi pa sigurado kung papaano namin gagawin, kung papaano namin i-e-elaborate ngayon dito sa budget, the P13-trillion debt, the problem on peace and order, the problem on corruption, and many more. Nasa ICU tayo, Sotto said in an interview Wednesday, November 10, on Rappler's election program On the Campaign Trail.(Yes, we're in the ICU. The pandemic, the debt, the Mandanas ruling which we still aren't certain how to handle, how to elaborate in the budget, the P13-trillion debt, the problem on peace and order, the problem on corruption, and many more. We are in the ICU.) The leader of a crucial voting bloc in the Senate since 2016, the start of his fourth term in the chamber, and the Senate president since 2018, Sotto has been criticized as an enabler of the Duterte administration, especially in its early years. The criticism extends to his running mate, Senator Panfilo Lacson. In an interview on the program On the Campaign Trail, which this writer hosts, he called the criticism silly. Asked if he agreed with this writers opening spiel – that the Philippines is undergoing what scholars call democratic decay, that we are in fact facing a crisis – he answered in this way: Yes, I do agree with what you say, but let me put it this way. If the Philippines is a patient, we are in the ICU. Then he added an election pitch: Now, if you are in the ICU, who will you choose for a doctor? Yung bagong graduate, o yung may expertise na? Ganoon yung thinking namin. (The new graduate, or the one with expertise? Thats our thinking.) Sotto has led the Senate in criticizing Health Secretary Francisco Duque III's handling of the pandemic, and questioning the work of the Inter-Agency Task Force, but has stopped short of directly calling out the chief executive. The Supreme Court's Mandanas ruling, set to finally take effect in 2022, affirms that local government units should share in all collections of national taxes, not just internally generated revenues. This will drastically increase the LGUs' share in the national budget but will also tax the resources of the national government. A report from the Congressional Policy and Budget Research Department outlined some of the difficult work ahead: Agency budgets during the transition period (2022-2024) will have to reflect changes following the devolution of certain programs/services, the shift in NG role from rowing to steering, and the movement and rationalization of personnel. Sotto's P13-trillion was a reference to the official government estimate of the national government's total outstanding debt by the end of 2022, or six months after the end of President Rodrigo Duterte's term. The Bureau of Treasury estimates that the country's debt stock will rise to an all-time high of P13.41 trillion, with about 70% of the debt, or P9.4 trillion, owed to domestic lenders. The P13 trillion is a doubling of the total outstanding debt inherited by President Duterte; in the last full year of the preceding administration, total debt stood at P6.6 trillion. Sotto commended the administration for doing creditable work on the enforcement aspect of the campaign against illegal drugs. To some extent, they have been successful. But he said it had failed in the other three aspects, of prosecution (There is much to be desired), prevention, and rehabilitation (the administration has done nothing, none at all). He was responding to a question about the seemingly selective PDEA raid on that Davao de Oro resort, which involved a close aide of Davao City Mayor Sara Duterte. Look at whats happening. Drugs are still proliferating.",

"You publicly criticize the President. No vice president should do that,' House Deputy Speaker Lito Atienza says of Vice President Leni Robredo Senator Manny Pacquiao running mate, House Deputy Speaker Lito Atienza, said that any vice president should not publicly criticize a sitting president even if they have differences. In a forum hosted by the Financial Executives Institute of the Philippines on Saturday, November 6, Atienza was asked about the role of a vice president. Atienza said that the vice president's role is not to be a heckler. And in answering the question, Atienza hit Vice President Leni Robredo for airing her criticisms of President Rodrigo Duterte in public. If I disagree with his program, I will talk to him in private, said Atienza if elected vice president. Never, never, never criticize him in public because you have just broken the line of working together. That's not good for the people. That's what we saw in the past six years. Atienza said that Robredo did not do what is right. You publicly criticize the President. No vice president should do that, he said. Robredo, a presidential aspirant and the face of the opposition, has been critical since the early days of the administration – on the issue of extrajudicial killings, the death penalty push, and the Marcos burial.",



]
    
    news_data = pd.read_csv('initial_news_data.csv', sep = ',', header=None)
    news_data_1 = news_data[0].str.split(',', expand=True)
    
    first = news_data_1[0].to_list()
    first = [x for x in first if x != None]
    first = [x for x in first if str(x) != None]
    first = [x for x in first if str(x) != 'nan']
    
    second = news_data_1[1].to_list()
    second = [x for x in second if x != None]
    second = [x for x in second if str(x) != None]
    second = [x for x in second if str(x) != 'nan']
    
    third = news_data_1[2].to_list()
    third = [x for x in third if x != None]
    third = [x for x in third if str(x) != None]
    third = [x for x in third if str(x) != 'nan']
    
    fourth = news_data_1[3].to_list()
    fourth = [x for x in fourth if x != None]
    fourth = [x for x in fourth if str(x) != None]
    fourth = [x for x in fourth if str(x) != 'nan']
    
    fifth = news_data_1[4].to_list()
    fifth = [x for x in fifth if x != None]
    fifth = [x for x in fifth if str(x) != None]
    fifth = [x for x in fifth if str(x) != 'nan']
    
    text = list(itertools.chain(text_init, first, second, third, fourth, fifth))
    text = text[:10000]
    
    df = co_occurrence(text, 30)
    dff = df.stack().reset_index()

    names = ['marcos', 'duterte', 'estrada', 'arroyo',
        'aquino', 'moreno', 'robredo', 'go',
        'lacson', 'pacquiao', 'guzman', 'atienza',
        'bello', 'ong', 'pangilinan', 'sotto']

    dfff = dff[(dff['level_0'].isin(names)) & (dff['level_1'].isin(names))]
    net = dfff
    net.columns = ['Target', 'Source', 'Frequency']
    net = net.reset_index(drop=True)
    
    G = nx.from_pandas_edgelist(net, 'Source', 'Target', ['Frequency'])
    
    degrees = dict(nx.degree(G))
    nx.set_node_attributes(G, name='degree', values=degrees)
    
    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree+number_to_adjust_by) for node, degree in nx.degree(G)])
    nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)
    
    weighted_degrees = dict(nx.degree(G, weight='Weight'))
    nx.set_node_attributes(G, name='weighted_degree', values=weighted_degrees)
    
    frequency = dict(nx.degree(G, weight='Frequency'))
    nx.set_node_attributes(G, name='frequency', values=frequency)
    
    emty = {}
    for i in range(len(net)):
        emty[(net['Target'][i],net['Source'][i])] = (net['Frequency'][i]/sum(net['Frequency']))*1000
    
    nx.set_edge_attributes(G, name='freq_degree', values=emty)
    
    betweenness_centrality = nx.betweenness_centrality(G)
    
    nx.set_node_attributes(G, name='betweenness', values=betweenness_centrality)
    
    communities = community.greedy_modularity_communities(G)
    communities = communities[:19]
    
    # Create empty dictionary
    modularity_class = {}
    modularity_color = {}
    #Loop through each community in the network
    for community_number, community in enumerate(communities):
        #For each member of the community, add their community number
        for name in community:
            modularity_class[name] = community_number
            modularity_color[name] = Category20c[20][community_number]
    
    nx.set_node_attributes(G, modularity_class, 'modularity_class')
    nx.set_node_attributes(G, modularity_color, 'modularity_color')
    
    #Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'modularity_color'
    
    node_highlight_color = 'white'
    edge_highlight_color = 'black'
    #Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    color_palette = Blues8
    
    #Choose a title!
    # title = 'BARMM Network'
    
    #Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
       ("Entity", "@index"),
       ("Degree", "@degree"),
       ("Frequency", "@frequency")
       ]
    
    #Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1))
    
    #Create a network graph object
    network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))
    
    #Set node sizes and colors according to node degree (color as category from attribute)
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
    #Set node highlight colors
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    
    
    #Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    
    #Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width="freq_degree")
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width="freq_degree")
    
    #Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()#EdgesAndLinkedNodes()
    
    plot.renderers.append(network_graph)
    st.bokeh_chart(plot)
    
elif add_selectbox == 'References':
    image1 = Image.open('explore.png')
    st.image(image1, caption='', use_column_width=True)