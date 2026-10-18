# Nguồn của từng bảng (sinh bởi scripts/make_report_tables.py)

Mọi bảng số liệu của báo cáo được sinh từ các tệp dưới đây; không sửa tay tệp .tex trong thư mục này.

| Tệp bảng | Nguồn |
|---|---|
| `tables/dataflow.tex` | results/figures/robustness/data_flow.csv (scripts/robustness.py) |
| `tables/quality.tex` | results/figures/report_manifest.json (các khóa <hệ thống>|random_test_all, |novel_premises_test_all) |
| `tables/signif.tex` | results/figures/robustness/significance_cluster.csv (scripts/robustness.py) |
| `tables/robust.tex` | results/figures/robustness/macro.csv, significance_cluster.csv; data/processed/eval_sets/random_holdoutB.json |
| `tables/unseen.tex` | results/figures/robustness/seen_unseen.csv (scripts/robustness.py) |
| `tables/controls.tex` | results/figures/report_manifest.json; results/figures/robustness/significance_cluster.csv |
| `tables/candidates.tex` | results/figures/robustness/candidates.csv (scripts/candidate_analysis.py) |
| `tables/v5grid.tex` | results/raw/tuning/V5__extra__random_val_all.csv (scripts/tune_v5.py); manifest V4|random_val_all |
| `tables/leandojo.tex` | Yang và cộng sự (2023), arXiv:2306.15626, Bảng 1 và Bảng B; manifest cho các dòng của nhóm |
| `tables/lucene.tex` | results/raw/lucene/*.json (scripts/lucene_baseline.py); manifest B0|random_test_all |
| `tables/v5load.tex` | results/raw/loadtest/*.json, tag v5cmp2-r* (run_scale.py --part serve_v5_k240) |
| `tables/workers.tex` | results/raw/loadtest/*.json tag workers-*; results/raw/serve-memory/*.json (run_scale.py --part serve2) |
| `tables/build.tex` | results/raw/build/*.json, experiment build2 (run_scale.py --part build2) |
| `tables/engines.tex` | results/raw/build/*.json (nhãn spark4, *-b0-arrow4, *-b0-rdd4) |
| `tables/profile.tex` | results/raw/profile/latency_profile.parquet (scripts/profile_latency.py) |
| `tables/errors.tex` | results/raw/error_analysis.parquet (scripts/error_analysis.py) |
| `tables/ablation.tex` | results/figures/ablation_significance.csv (scripts/ablation_significance.py) |
| `tables/example.tex` | scripts/running_example.py (top 100 của các lần chạy validation đã ghim) |

## Lần chạy đánh giá đã ghim (results/figures/report_manifest.json)

| Hệ thống và tập | run_id |
|---|---|
| B0t|novel_premises_test_all | `eval-B0t-20261017-185614-972d` |
| B0t|random_test_all | `eval-B0t-20261017-185614-7077` |
| B0t|random_val_all | `eval-B0t-20261017-190342-2da0` |
| B0|novel_premises_test_all | `eval-B0-20261017-185614-f8f5` |
| B0|random_holdoutB | `eval-B0-20261018-230121-0d0f` |
| B0|random_test_all | `eval-B0-20261017-185614-87d3` |
| B0|random_val_all | `eval-B0-20261017-182139-babd` |
| V1|novel_premises_test_all | `eval-V1-20261017-185614-0219` |
| V1|random_test_all | `eval-V1-20261017-185614-ddf0` |
| V1|random_val_all | `eval-V1-20261017-190342-db6a` |
| V2-nons|novel_premises_test_all | `eval-V2-nons-20261018-225532-e547` |
| V2-nons|random_test_all | `eval-V2-nons-20261018-225435-5906` |
| V2-nons|random_val_all | `eval-V2-nons-20261018-225342-8659` |
| V2a|novel_premises_test_all | `eval-V2a-20261017-194917-d3b1` |
| V2a|random_test_all | `eval-V2a-20261017-194917-a4da` |
| V2a|random_val_all | `eval-V2a-20261017-194917-a6ad` |
| V2|novel_premises_test_all | `eval-V2-20261017-185715-2809` |
| V2|random_holdoutB | `eval-V2-20261018-230154-aeae` |
| V2|random_test_all | `eval-V2-20261017-185714-d412` |
| V2|random_val_all | `eval-V2-20261017-190342-2f5f` |
| V3|novel_premises_test_all | `eval-V3-20261017-185759-7ab2` |
| V3|random_test_all | `eval-V3-20261017-185747-0e83` |
| V3|random_val_all | `eval-V3-20261017-185233-51c7` |
| V4-K240|novel_premises_test_all | `eval-V4-K240-20261018-225059-9a90` |
| V4-K240|random_holdoutB | `eval-V4-K240-20261018-225243-bb3c` |
| V4-K240|random_test_all | `eval-V4-K240-20261018-224951-837e` |
| V4-K240|random_val_all | `eval-V4-K240-20261018-224846-fba9` |
| V4-poponly|random_test_all | `eval-V4-poponly-20261018-225806-d905` |
| V4-poponly|random_val_all | `eval-V4-poponly-20261018-225703-5221` |
| V4-pronly|random_test_all | `eval-V4-pronly-20261018-230015-05d2` |
| V4-pronly|random_val_all | `eval-V4-pronly-20261018-225911-29a5` |
| V4|novel_premises_test_all | `eval-V4-20261017-194917-35a4` |
| V4|random_holdoutB | `eval-V4-20261018-230243-b493` |
| V4|random_test_all | `eval-V4-20261018-214227-6e88` |
| V4|random_val_all | `eval-V4-20261017-194917-ebac` |
| V5|novel_premises_test_all | `eval-V5-20261018-220757-26a7` |
| V5|random_holdoutB | `eval-V5-20261018-230340-4bf3` |
| V5|random_test_all | `eval-V5-20261018-220652-4f11` |
| V5|random_val_all | `eval-V5-20261018-220552-dadd` |
