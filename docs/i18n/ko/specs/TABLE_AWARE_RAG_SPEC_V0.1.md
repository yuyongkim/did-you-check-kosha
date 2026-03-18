# Table-Aware RAG Specification (한국어)

> 원문 기준 문서: `docs/specs\TABLE_AWARE_RAG_SPEC_V0.1.md`
> English companion: `docs/specs\TABLE_AWARE_RAG_SPEC_V0.1.en.md`

## 문서 목적
이 문서는 원문 문서의 한국어 동반본입니다. 공식 기준은 원문의 수식, 수치, 표준 조항, 코드 구현입니다.

## 섹션 맵 (원문 헤더)
- Context Summary
- Architecture Overview
- Detailed Specifications
- 1) End-to-End Architecture Diagram
- 2) Document Preprocessing Pipeline
- 2.1 Input and Normalization
- 2.2 Structural Extraction
- 2.3 Chunking Strategy
- 3) Index and Retrieval Strategy
- 3.1 Index Partitioning
- 3.2 Hybrid Retrieval
- 3.3 Retrieval Pseudocode
- 4) Condition-Aware Value Extraction
- 5) Spec Explorer API Contract
- 5.1 `search_standard`
- 5.2 `extract_table_value`
- 5.3 `resolve_cross_reference`
- 6) Caching and Performance Optimization
- 7) Data Quality and Validation
- 8) Failure Modes and Fallback
- 9) Integration Constraints
- Verification Strategy
- Performance and Accuracy Targets
- Next Steps

## 한국어 운영 요약
- 본 문서는 `Table-Aware RAG Specification` 주제를 다룹니다.
- 계산/검증 판단 시 원문의 값과 표준 참조를 우선하십시오.
- 상세 수식/표/예외 조건은 원문에서 직접 확인하십시오.

## 원문/영문 링크
- Source: `docs/specs\TABLE_AWARE_RAG_SPEC_V0.1.md`
- English: `docs/specs\TABLE_AWARE_RAG_SPEC_V0.1.en.md`
- Korean: `docs/specs\TABLE_AWARE_RAG_SPEC_V0.1.ko.md`

