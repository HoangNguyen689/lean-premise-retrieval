# Phân tích độ bền (sinh bởi scripts/robustness.py từ results/figures/report_manifest.json)

## 1. Luồng lọc dữ liệu

| split | tập | theorem_gốc | theorem_có_tactic | theorem_có_tactic_có_premise | tactic | tactic_có_premise | nhãn_không_có_trong_corpus | truy_vấn_bị_loại | truy_vấn_giữ_lại | theorem_còn_truy_vấn | tỉ_lệ_theorem_giữ_lại | proof_state_khác_nhau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| random | train | 118517 | 59557 | 53787 | 250814 | 162262 | 55971 | 9932 | 152330 | 52663 | 0.4440 | 151134 |
| random | val | 2000 | 995 | 892 | 4260 | 2681 | 867 | 145 | 2536 | 880 | 0.4400 | 2530 |
| random | test | 2000 | 992 | 898 | 4506 | 2836 | 1030 | 195 | 2641 | 882 | 0.4410 | 2623 |
| novel_premises | train | 118517 | 59050 | 53154 | 246714 | 159234 | 54047 | 9775 | 149459 | 52047 | 0.4390 | 148288 |
| novel_premises | val | 2000 | 1245 | 1207 | 6240 | 4165 | 1886 | 258 | 3907 | 1182 | 0.5910 | 3876 |
| novel_premises | test | 2000 | 1249 | 1216 | 6626 | 4380 | 1935 | 239 | 4141 | 1196 | 0.5980 | 4109 |

Tổng số lượt truy vấn của hai split là 315,014; số proof state khác nhau trong từng split: {'novel_premises': 156258, 'random': 156258}.

## 2. Trung bình theo truy vấn và theo theorem

| Tập | Hệ thống | Truy vấn | Theorem | R@10 (truy vấn) | R@10 (theorem) | MRR (truy vấn) | MRR (theorem) |
|---|---|---|---|---|---|---|---|
| random_test_all | B0 | 2641 | 882 | 0.1004 | 0.1506 | 0.0654 | 0.0999 |
| random_test_all | B0t | 2641 | 882 | 0.1238 | 0.1821 | 0.0784 | 0.1191 |
| random_test_all | V1 | 2641 | 882 | 0.1342 | 0.1958 | 0.0866 | 0.1279 |
| random_test_all | V2 | 2641 | 882 | 0.1470 | 0.2185 | 0.0927 | 0.1365 |
| random_test_all | V2-nons | 2641 | 882 | 0.1457 | 0.2156 | 0.0926 | 0.1378 |
| random_test_all | V3 | 2641 | 882 | 0.1683 | 0.2624 | 0.1124 | 0.1738 |
| random_test_all | V2a | 2641 | 882 | 0.1826 | 0.2693 | 0.1480 | 0.2349 |
| random_test_all | V4 | 2641 | 882 | 0.2425 | 0.3586 | 0.1956 | 0.3087 |
| random_test_all | V4-poponly | 2641 | 882 | 0.2442 | 0.3599 | 0.1956 | 0.3090 |
| random_test_all | V4-pronly | 2641 | 882 | 0.2437 | 0.3650 | 0.1913 | 0.3086 |
| random_test_all | V4-K240 | 2641 | 882 | 0.2537 | 0.3720 | 0.2016 | 0.3137 |
| random_test_all | V5 | 2641 | 882 | 0.2807 | 0.3931 | 0.2166 | 0.3230 |
| novel_premises_test_all | B0 | 4141 | 1196 | 0.1275 | 0.1978 | 0.0899 | 0.1343 |
| novel_premises_test_all | B0t | 4141 | 1196 | 0.1546 | 0.2238 | 0.1056 | 0.1458 |
| novel_premises_test_all | V1 | 4141 | 1196 | 0.1628 | 0.2322 | 0.1099 | 0.1459 |
| novel_premises_test_all | V2 | 4141 | 1196 | 0.1826 | 0.2530 | 0.1238 | 0.1630 |
| novel_premises_test_all | V2-nons | 4141 | 1196 | 0.1801 | 0.2488 | 0.1224 | 0.1613 |
| novel_premises_test_all | V3 | 4141 | 1196 | 0.2049 | 0.2961 | 0.1401 | 0.1942 |
| novel_premises_test_all | V2a | 4141 | 1196 | 0.2212 | 0.3076 | 0.1758 | 0.2519 |
| novel_premises_test_all | V4 | 4141 | 1196 | 0.2695 | 0.3725 | 0.2108 | 0.3035 |
| novel_premises_test_all | V4-K240 | 4141 | 1196 | 0.2762 | 0.3774 | 0.2124 | 0.3016 |
| novel_premises_test_all | V5 | 4141 | 1196 | 0.2802 | 0.3585 | 0.2154 | 0.2869 |
| random_holdoutB | B0 | 2500 | 1138 | 0.1131 | 0.1335 | 0.0708 | 0.0851 |
| random_holdoutB | V2 | 2500 | 1138 | 0.1896 | 0.2155 | 0.1207 | 0.1400 |
| random_holdoutB | V4 | 2500 | 1138 | 0.3102 | 0.3712 | 0.2460 | 0.3105 |
| random_holdoutB | V4-K240 | 2500 | 1138 | 0.3212 | 0.3811 | 0.2548 | 0.3166 |
| random_holdoutB | V5 | 2500 | 1138 | 0.3323 | 0.3882 | 0.2609 | 0.3201 |

## 3. Kiểm định bootstrap theo cụm theorem (10.000 mẫu)

KTC từ bootstrap theo cụm; p hai phía từ kiểm định hoán vị theo cụm. Họ chính: Holm trong từng tập, metric và cách lấy trung bình. Họ phụ: không hiệu chỉnh.

| Tập | Họ | So sánh | Metric | Trung bình | Δ | KTC 95% | p | p Holm |
|---|---|---|---|---|---|---|---|---|
| random_test_all | chính | B0 → B0t | R@10 | truy vấn | +0.0233 | [+0.0132; +0.0332] | 0.0001 | 0.0007 |
| random_test_all | chính | B0 → B0t | R@10 | theorem | +0.0315 | [+0.0167; +0.0464] | 0.0001 | 0.0007 |
| random_test_all | chính | B0 → B0t | MRR | truy vấn | +0.0130 | [+0.0072; +0.0193] | 0.0001 | 0.0007 |
| random_test_all | chính | B0 → B0t | MRR | theorem | +0.0191 | [+0.0094; +0.0290] | 0.0002 | 0.0008 |
| random_test_all | chính | B0t → V1 | R@10 | truy vấn | +0.0105 | [+0.0001; +0.0217] | 0.0527 | 0.0527 |
| random_test_all | chính | B0t → V1 | R@10 | theorem | +0.0137 | [-0.0012; +0.0290] | 0.0781 | 0.0781 |
| random_test_all | chính | B0t → V1 | MRR | truy vấn | +0.0082 | [+0.0020; +0.0144] | 0.0095 | 0.0095 |
| random_test_all | chính | B0t → V1 | MRR | theorem | +0.0088 | [-0.0020; +0.0198] | 0.1085 | 0.1085 |
| random_test_all | chính | V1 → V2 | R@10 | truy vấn | +0.0128 | [+0.0059; +0.0202] | 0.0003 | 0.0007 |
| random_test_all | chính | V1 → V2 | R@10 | theorem | +0.0228 | [+0.0134; +0.0325] | 0.0001 | 0.0007 |
| random_test_all | chính | V1 → V2 | MRR | truy vấn | +0.0061 | [+0.0023; +0.0101] | 0.0013 | 0.0026 |
| random_test_all | chính | V1 → V2 | MRR | theorem | +0.0086 | [+0.0030; +0.0145] | 0.0032 | 0.0096 |
| random_test_all | chính | V2 → V3 | R@10 | truy vấn | +0.0213 | [+0.0103; +0.0325] | 0.0002 | 0.0007 |
| random_test_all | chính | V2 → V3 | R@10 | theorem | +0.0439 | [+0.0278; +0.0601] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V3 | MRR | truy vấn | +0.0197 | [+0.0135; +0.0263] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V3 | MRR | theorem | +0.0373 | [+0.0289; +0.0461] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V2a | R@10 | truy vấn | +0.0356 | [+0.0287; +0.0435] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V2a | R@10 | theorem | +0.0508 | [+0.0412; +0.0612] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V2a | MRR | truy vấn | +0.0553 | [+0.0483; +0.0629] | 0.0001 | 0.0007 |
| random_test_all | chính | V2 → V2a | MRR | theorem | +0.0984 | [+0.0867; +0.1105] | 0.0001 | 0.0007 |
| random_test_all | chính | V2a → V4 | R@10 | truy vấn | +0.0599 | [+0.0456; +0.0742] | 0.0001 | 0.0007 |
| random_test_all | chính | V2a → V4 | R@10 | theorem | +0.0893 | [+0.0702; +0.1085] | 0.0001 | 0.0007 |
| random_test_all | chính | V2a → V4 | MRR | truy vấn | +0.0476 | [+0.0394; +0.0561] | 0.0001 | 0.0007 |
| random_test_all | chính | V2a → V4 | MRR | theorem | +0.0737 | [+0.0598; +0.0882] | 0.0001 | 0.0007 |
| random_test_all | chính | V4 → V5 | R@10 | truy vấn | +0.0382 | [+0.0244; +0.0526] | 0.0001 | 0.0007 |
| random_test_all | chính | V4 → V5 | R@10 | theorem | +0.0344 | [+0.0174; +0.0516] | 0.0002 | 0.0007 |
| random_test_all | chính | V4 → V5 | MRR | truy vấn | +0.0210 | [+0.0115; +0.0306] | 0.0001 | 0.0007 |
| random_test_all | chính | V4 → V5 | MRR | theorem | +0.0143 | [+0.0007; +0.0281] | 0.0427 | 0.0854 |
| random_test_all | phụ | B0 → V4 | R@10 | truy vấn | +0.1421 | [+0.1265; +0.1583] | 0.0001 |  |
| random_test_all | phụ | B0 → V4 | R@10 | theorem | +0.2080 | [+0.1853; +0.2307] | 0.0001 |  |
| random_test_all | phụ | B0 → V4 | MRR | truy vấn | +0.1302 | [+0.1163; +0.1453] | 0.0001 |  |
| random_test_all | phụ | B0 → V4 | MRR | theorem | +0.2087 | [+0.1889; +0.2288] | 0.0001 |  |
| random_test_all | phụ | B0 → V5 | R@10 | truy vấn | +0.1803 | [+0.1620; +0.1998] | 0.0001 |  |
| random_test_all | phụ | B0 → V5 | R@10 | theorem | +0.2425 | [+0.2197; +0.2659] | 0.0001 |  |
| random_test_all | phụ | B0 → V5 | MRR | truy vấn | +0.1512 | [+0.1361; +0.1677] | 0.0001 |  |
| random_test_all | phụ | B0 → V5 | MRR | theorem | +0.2231 | [+0.2015; +0.2446] | 0.0001 |  |
| random_test_all | phụ | V4 → V4-K240 | R@10 | truy vấn | +0.0112 | [+0.0037; +0.0188] | 0.0038 |  |
| random_test_all | phụ | V4 → V4-K240 | R@10 | theorem | +0.0134 | [+0.0011; +0.0253] | 0.0267 |  |
| random_test_all | phụ | V4 → V4-K240 | MRR | truy vấn | +0.0060 | [+0.0018; +0.0103] | 0.0051 |  |
| random_test_all | phụ | V4 → V4-K240 | MRR | theorem | +0.0051 | [-0.0026; +0.0128] | 0.2008 |  |
| random_test_all | phụ | V4-K240 → V5 | R@10 | truy vấn | +0.0270 | [+0.0138; +0.0408] | 0.0002 |  |
| random_test_all | phụ | V4-K240 → V5 | R@10 | theorem | +0.0210 | [+0.0045; +0.0379] | 0.0157 |  |
| random_test_all | phụ | V4-K240 → V5 | MRR | truy vấn | +0.0150 | [+0.0049; +0.0249] | 0.0025 |  |
| random_test_all | phụ | V4-K240 → V5 | MRR | theorem | +0.0093 | [-0.0039; +0.0227] | 0.1827 |  |
| random_test_all | phụ | V2-nons → V2 | R@10 | truy vấn | +0.0014 | [-0.0025; +0.0049] | 0.4933 |  |
| random_test_all | phụ | V2-nons → V2 | R@10 | theorem | +0.0030 | [-0.0012; +0.0077] | 0.1983 |  |
| random_test_all | phụ | V2-nons → V2 | MRR | truy vấn | +0.0002 | [-0.0010; +0.0015] | 0.7974 |  |
| random_test_all | phụ | V2-nons → V2 | MRR | theorem | -0.0013 | [-0.0038; +0.0010] | 0.3022 |  |
| random_test_all | phụ | V4-poponly → V4 | R@10 | truy vấn | -0.0016 | [-0.0037; +0.0001] | 0.1133 |  |
| random_test_all | phụ | V4-poponly → V4 | R@10 | theorem | -0.0013 | [-0.0035; +0.0006] | 0.2256 |  |
| random_test_all | phụ | V4-poponly → V4 | MRR | truy vấn | -0.0000 | [-0.0013; +0.0012] | 0.9386 |  |
| random_test_all | phụ | V4-poponly → V4 | MRR | theorem | -0.0003 | [-0.0032; +0.0027] | 0.8416 |  |
| random_test_all | phụ | V4-pronly → V4 | R@10 | truy vấn | -0.0011 | [-0.0081; +0.0058] | 0.7497 |  |
| random_test_all | phụ | V4-pronly → V4 | R@10 | theorem | -0.0064 | [-0.0152; +0.0024] | 0.1623 |  |
| random_test_all | phụ | V4-pronly → V4 | MRR | truy vấn | +0.0043 | [-0.0001; +0.0087] | 0.0626 |  |
| random_test_all | phụ | V4-pronly → V4 | MRR | theorem | +0.0001 | [-0.0084; +0.0086] | 0.9896 |  |
| novel_premises_test_all | chính | B0 → B0t | R@10 | truy vấn | +0.0271 | [+0.0189; +0.0354] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | B0 → B0t | R@10 | theorem | +0.0260 | [+0.0133; +0.0391] | 0.0004 | 0.0012 |
| novel_premises_test_all | chính | B0 → B0t | MRR | truy vấn | +0.0157 | [+0.0093; +0.0220] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | B0 → B0t | MRR | theorem | +0.0115 | [+0.0022; +0.0203] | 0.0105 | 0.0210 |
| novel_premises_test_all | chính | B0t → V1 | R@10 | truy vấn | +0.0082 | [+0.0003; +0.0161] | 0.0470 | 0.0940 |
| novel_premises_test_all | chính | B0t → V1 | R@10 | theorem | +0.0084 | [-0.0039; +0.0206] | 0.1742 | 0.1742 |
| novel_premises_test_all | chính | B0t → V1 | MRR | truy vấn | +0.0044 | [-0.0016; +0.0101] | 0.1367 | 0.2734 |
| novel_premises_test_all | chính | B0t → V1 | MRR | theorem | +0.0001 | [-0.0088; +0.0091] | 0.9785 | 0.9785 |
| novel_premises_test_all | chính | V1 → V2 | R@10 | truy vấn | +0.0198 | [+0.0126; +0.0273] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V1 → V2 | R@10 | theorem | +0.0208 | [+0.0116; +0.0301] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V1 → V2 | MRR | truy vấn | +0.0139 | [+0.0089; +0.0190] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V1 → V2 | MRR | theorem | +0.0171 | [+0.0119; +0.0224] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V3 | R@10 | truy vấn | +0.0223 | [+0.0122; +0.0323] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V3 | R@10 | theorem | +0.0431 | [+0.0300; +0.0563] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V3 | MRR | truy vấn | +0.0163 | [+0.0108; +0.0217] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V3 | MRR | theorem | +0.0312 | [+0.0225; +0.0402] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V2a | R@10 | truy vấn | +0.0386 | [+0.0324; +0.0452] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V2a | R@10 | theorem | +0.0546 | [+0.0459; +0.0640] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V2a | MRR | truy vấn | +0.0520 | [+0.0466; +0.0579] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2 → V2a | MRR | theorem | +0.0889 | [+0.0803; +0.0974] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2a → V4 | R@10 | truy vấn | +0.0483 | [+0.0375; +0.0593] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2a → V4 | R@10 | theorem | +0.0649 | [+0.0509; +0.0791] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2a → V4 | MRR | truy vấn | +0.0350 | [+0.0282; +0.0419] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V2a → V4 | MRR | theorem | +0.0516 | [+0.0409; +0.0626] | 0.0001 | 0.0007 |
| novel_premises_test_all | chính | V4 → V5 | R@10 | truy vấn | +0.0107 | [-0.0005; +0.0223] | 0.0742 | 0.0940 |
| novel_premises_test_all | chính | V4 → V5 | R@10 | theorem | -0.0139 | [-0.0263; -0.0018] | 0.0265 | 0.0530 |
| novel_premises_test_all | chính | V4 → V5 | MRR | truy vấn | +0.0046 | [-0.0027; +0.0121] | 0.2405 | 0.2734 |
| novel_premises_test_all | chính | V4 → V5 | MRR | theorem | -0.0166 | [-0.0261; -0.0068] | 0.0010 | 0.0030 |
| novel_premises_test_all | phụ | B0 → V4 | R@10 | truy vấn | +0.1420 | [+0.1281; +0.1565] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V4 | R@10 | theorem | +0.1747 | [+0.1581; +0.1917] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V4 | MRR | truy vấn | +0.1208 | [+0.1094; +0.1330] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V4 | MRR | theorem | +0.1692 | [+0.1535; +0.1849] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V5 | R@10 | truy vấn | +0.1527 | [+0.1379; +0.1685] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V5 | R@10 | theorem | +0.1607 | [+0.1432; +0.1785] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V5 | MRR | truy vấn | +0.1255 | [+0.1141; +0.1373] | 0.0001 |  |
| novel_premises_test_all | phụ | B0 → V5 | MRR | theorem | +0.1526 | [+0.1371; +0.1680] | 0.0001 |  |
| novel_premises_test_all | phụ | V4 → V4-K240 | R@10 | truy vấn | +0.0067 | [+0.0019; +0.0117] | 0.0084 |  |
| novel_premises_test_all | phụ | V4 → V4-K240 | R@10 | theorem | +0.0050 | [-0.0023; +0.0123] | 0.1817 |  |
| novel_premises_test_all | phụ | V4 → V4-K240 | MRR | truy vấn | +0.0017 | [-0.0013; +0.0048] | 0.2826 |  |
| novel_premises_test_all | phụ | V4 → V4-K240 | MRR | theorem | -0.0019 | [-0.0065; +0.0027] | 0.4251 |  |
| novel_premises_test_all | phụ | V4-K240 → V5 | R@10 | truy vấn | +0.0040 | [-0.0076; +0.0158] | 0.5006 |  |
| novel_premises_test_all | phụ | V4-K240 → V5 | R@10 | theorem | -0.0189 | [-0.0311; -0.0067] | 0.0022 |  |
| novel_premises_test_all | phụ | V4-K240 → V5 | MRR | truy vấn | +0.0030 | [-0.0039; +0.0099] | 0.4096 |  |
| novel_premises_test_all | phụ | V4-K240 → V5 | MRR | theorem | -0.0147 | [-0.0238; -0.0052] | 0.0017 |  |
| novel_premises_test_all | phụ | V2-nons → V2 | R@10 | truy vấn | +0.0025 | [+0.0003; +0.0047] | 0.0298 |  |
| novel_premises_test_all | phụ | V2-nons → V2 | R@10 | theorem | +0.0042 | [+0.0005; +0.0082] | 0.0288 |  |
| novel_premises_test_all | phụ | V2-nons → V2 | MRR | truy vấn | +0.0014 | [+0.0002; +0.0026] | 0.0243 |  |
| novel_premises_test_all | phụ | V2-nons → V2 | MRR | theorem | +0.0017 | [-0.0006; +0.0038] | 0.1416 |  |
| random_holdoutB | chính | V4 → V5 | R@10 | truy vấn | +0.0222 | [+0.0094; +0.0349] | 0.0010 | 0.0010 |
| random_holdoutB | chính | V4 → V5 | R@10 | theorem | +0.0170 | [+0.0022; +0.0323] | 0.0250 | 0.0250 |
| random_holdoutB | chính | V4 → V5 | MRR | truy vấn | +0.0148 | [+0.0069; +0.0230] | 0.0006 | 0.0006 |
| random_holdoutB | chính | V4 → V5 | MRR | theorem | +0.0096 | [-0.0018; +0.0211] | 0.0988 | 0.0988 |
| random_holdoutB | phụ | B0 → V4 | R@10 | truy vấn | +0.1971 | [+0.1809; +0.2144] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V4 | R@10 | theorem | +0.2377 | [+0.2183; +0.2575] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V4 | MRR | truy vấn | +0.1753 | [+0.1609; +0.1902] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V4 | MRR | theorem | +0.2253 | [+0.2068; +0.2443] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V5 | R@10 | truy vấn | +0.2193 | [+0.2026; +0.2372] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V5 | R@10 | theorem | +0.2547 | [+0.2345; +0.2759] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V5 | MRR | truy vấn | +0.1901 | [+0.1756; +0.2050] | 0.0001 |  |
| random_holdoutB | phụ | B0 → V5 | MRR | theorem | +0.2350 | [+0.2164; +0.2540] | 0.0001 |  |
| random_holdoutB | phụ | V4 → V4-K240 | R@10 | truy vấn | +0.0110 | [+0.0039; +0.0183] | 0.0025 |  |
| random_holdoutB | phụ | V4 → V4-K240 | R@10 | theorem | +0.0099 | [+0.0002; +0.0200] | 0.0461 |  |
| random_holdoutB | phụ | V4 → V4-K240 | MRR | truy vấn | +0.0088 | [+0.0045; +0.0131] | 0.0002 |  |
| random_holdoutB | phụ | V4 → V4-K240 | MRR | theorem | +0.0061 | [+0.0008; +0.0119] | 0.0272 |  |
| random_holdoutB | phụ | V4-K240 → V5 | R@10 | truy vấn | +0.0111 | [-0.0017; +0.0239] | 0.0983 |  |
| random_holdoutB | phụ | V4-K240 → V5 | R@10 | theorem | +0.0071 | [-0.0072; +0.0217] | 0.3426 |  |
| random_holdoutB | phụ | V4-K240 → V5 | MRR | truy vấn | +0.0061 | [-0.0023; +0.0146] | 0.1602 |  |
| random_holdoutB | phụ | V4-K240 → V5 | MRR | theorem | +0.0035 | [-0.0082; +0.0152] | 0.5607 |  |

## 4. Premise đã thấy và chưa thấy trong train cùng split

| tập | cặp_nhãn | cặp_chưa_thấy | premise_chưa_thấy_khác_nhau | truy_vấn_có_nhãn_chưa_thấy | theorem_có_nhãn_chưa_thấy | theorem_được_chấm | hệ_thống | R@10_chưa_thấy | R@10_đã_thấy | R@50_chưa_thấy | R@50_đã_thấy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random_test_all | 5483 | 598 | 490 | 517 | 314 | 882 | B0 | 0.2832 | 0.0669 | 0.4453 | 0.1286 |
| random_test_all | 5483 | 598 | 490 | 517 | 314 | 882 | V2 | 0.3858 | 0.1049 | 0.5960 | 0.2146 |
| random_test_all | 5483 | 598 | 490 | 517 | 314 | 882 | V4 | 0.4102 | 0.2118 | 0.6591 | 0.3253 |
| random_test_all | 5483 | 598 | 490 | 517 | 314 | 882 | V4-K240 | 0.3902 | 0.2280 | 0.6299 | 0.3811 |
| random_test_all | 5483 | 598 | 490 | 517 | 314 | 882 | V5 | 0.3401 | 0.2657 | 0.5439 | 0.4941 |
| novel_premises_test_all | 9735 | 2506 | 1933 | 1887 | 1093 | 1196 | B0 | 0.2925 | 0.0440 | 0.4427 | 0.1012 |
| novel_premises_test_all | 9735 | 2506 | 1933 | 1887 | 1093 | 1196 | V2 | 0.3560 | 0.0922 | 0.6034 | 0.2053 |
| novel_premises_test_all | 9735 | 2506 | 1933 | 1887 | 1093 | 1196 | V4 | 0.4442 | 0.1784 | 0.6896 | 0.2863 |
| novel_premises_test_all | 9735 | 2506 | 1933 | 1887 | 1093 | 1196 | V4-K240 | 0.4276 | 0.1934 | 0.6823 | 0.3352 |
| novel_premises_test_all | 9735 | 2506 | 1933 | 1887 | 1093 | 1196 | V5 | 0.3591 | 0.2305 | 0.6033 | 0.4508 |

| tập | từ | đến | metric | delta | ci95_low | ci95_high | n_clusters | n_boot | p |
|---|---|---|---|---|---|---|---|---|---|
| random_test_all | V4 | V5 | R@10_chưa_thấy | -0.0701 | -0.0980 | -0.0436 | 314 | 10000 | 0.0001 |
| random_test_all | V4 | V4-K240 | R@10_chưa_thấy | -0.0200 | -0.0381 | -0.0036 | 314 | 10000 | 0.0286 |
| random_test_all | V4-K240 | V5 | R@10_chưa_thấy | -0.0501 | -0.0769 | -0.0239 | 314 | 10000 | 0.0003 |
| novel_premises_test_all | V4 | V5 | R@10_chưa_thấy | -0.0850 | -0.0997 | -0.0710 | 1093 | 10000 | 0.0001 |
| novel_premises_test_all | V4 | V4-K240 | R@10_chưa_thấy | -0.0166 | -0.0258 | -0.0075 | 1093 | 10000 | 0.0005 |
| novel_premises_test_all | V4-K240 | V5 | R@10_chưa_thấy | -0.0684 | -0.0819 | -0.0553 | 1093 | 10000 | 0.0001 |

## 5. Theo số truy vấn của theorem (R@10 trung bình theo truy vấn trong nhóm)

| tập | nhóm_số_truy_vấn | n_theorem | n_truy_vấn | R@10_V4 | R@10_V4-K240 | R@10_V5 |
|---|---|---|---|---|---|---|
| random_test_all | 1 | 449 | 449 | 0.4632 | 0.4703 | 0.4755 |
| random_test_all | 2-4 | 295 | 753 | 0.2761 | 0.2975 | 0.3382 |
| random_test_all | >=5 | 138 | 1439 | 0.1561 | 0.1633 | 0.1899 |
| novel_premises_test_all | 1 | 536 | 536 | 0.4467 | 0.4501 | 0.4075 |
| novel_premises_test_all | 2-4 | 420 | 1080 | 0.3492 | 0.3522 | 0.3469 |
| novel_premises_test_all | >=5 | 240 | 2525 | 0.1977 | 0.2068 | 0.2246 |
| random_holdoutB | 1 | 630 | 630 | 0.4126 | 0.4222 | 0.4288 |
| random_holdoutB | 2-4 | 396 | 1048 | 0.3314 | 0.3442 | 0.3500 |
| random_holdoutB | >=5 | 112 | 822 | 0.2045 | 0.2145 | 0.2359 |
