<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# Software System Test Plan

> `SR ID` refers to the ID of the software requirement which is tested by this test.

> Note that this is, strictly speaking, not a "plan" because it already includes the results (columns "Actual"
> and "Pass?"). To keep things clean, I'd suggest splitting this table up into a "plan" and a "protocol"
> (suggestion by a friendly auditor). The plan contains all columns below except "Actual" and
> "Pass?". The protocol contains all columns. The idea is this: It makes sense to write the plan before
> actually doing the testing. You don't want to be changing the test steps when you notice your tests are
> failing (surely nobody would do that). So you write the plan first, finalize it, then copy-paste it to a
> protocol in which you enter the results after you've done your tests.

| ID  | SR ID | Description                                    | Steps                                                                          | Expected                              | Actual                      | Pass? |
| --- | ----- | ---------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------- | --------------------------- | ----- |
| 1   | 1     | Login with correct email and password succeeds | 1. Enter email steve@apple.com<br>2. Enter password atari<br>3. Click login    | Redirect to account page              | Redirect to account page    | Pass  |
| 2   | 1     | Login with incorrect email and password fails  | 1. Enter email jony@apple.com<br>2. Enter password butterfly<br>3. Click login | Error "invalid credentials" displayed | Error "invalid credentials" | Pass  |
