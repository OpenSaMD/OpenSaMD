---
id: TESTREC-001
title: Software Test Record
---

# Software Test Record

## Purpose

The purpose of this document is to record the status of the software tests run for Radiotherapy AI Contour Recommendations.

## Scope

The scope of this document is the software system within the Radiotherapy AI Contour Recommendations product.

## Verification

I, FULL DEVELOPER NAME, verify that the results recorded here are complete and accurate [[62304:9.8.g]].

TODO: document the identity of the tester if any manual steps were required.

Tests were performed on DATE TESTS COMPLETED.
TODO: document the date tested [[62304:9.8.f]]

The tests meet our specified pass fail criteria (see Test Plan section of the Software Plan).

## Test Environment

TODO: Describe the test environment. This section should include all of the information necessary for someone to reproduce the tests. For example, it could be wise to include a list of all the environment variables, installed system packages and versions, the git hash, hardware used, etc. It should also include any relevant testing tools [[62304:5.1.11]].
TODO: document the software version tested [[62304:9.8.c]]
TODO: document any relevant configuration [[62304:9.8.d]]
TODO: document the relevant tools used to run these tests [[62304:9.8.e]]

## Test Results

[[These are the results of automated unit and integration testing as well as manual testing 62304:9.8.a]]
TODO: List of all the tests, split into sections by type. You can use the three subsections below as a starting point.

TODO: List any problems that were found during testing, and, if relevant, the problem report ids.
TODO: document any anomilies encountered [[62304:9.8.b]]

It is ok if some tests do not trace to any particular requirements, however all requirements must be covered by some tests (if they are not, add tests).

### Unit Tests

| Test Name | Test Status | Requirement IDs | Notes |
| --------- | ----------- | --------------- | ----- |
| TestClass.TestName1 | pass | ['SR-12'] |  |
| TestClass.TestName2 | fail | ['SR-12'] | It is okay that this test failed because of XYZ |


### Integration Tests

| Test Name | Test Status | Requirement IDs | Notes |
| --------- | ----------- | --------------- | ----- |
| TestClass.TestName100 | pass | ['SR-13', 'SR-14'] |  |
| TestClass.TestName200 | fail | ['SR-17'] | It is okay that this test failed because of XYZ |
| TestClass.TestName300 | pass | ['SR-17'] |  |


### Manual Tests

| Test Name | Step | Test Status | Requirement IDs | Notes |
| --------- | ---- | ----------- | --------------- | ----- |
| ManualTest1 | 5 | pass | ['SR-18'] |  |
| ManualTest1 | 6 | fail | ['SR-19'] | Allowed because of XYZ |
| ManualTest2 | 1 | pass | ['SR-11', 'SR-12'] |  |
