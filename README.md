# stackspot-ai-rqc

[![Action Test Ubuntu](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-ubuntu.yaml/badge.svg)](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-ubuntu.yaml) [![Action Test MacOS](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-macos.yaml/badge.svg)](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-macos.yaml) [![Action Test Windows](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-windows.yaml/badge.svg)](https://github.com/GuillaumeFalourd/stackspot-ai-rqc/actions/workflows/action-test-windows.yaml)

StackSpot AI Remote Quick Command Action

This action forwards an `input_data` to a [StackSpot AI remote quick command](https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc) and returns a JSON as answer (github action output) to be manipulated in future steps for customizable operations.

_Note: This action is supported on all operating systems._

## Usage

```yaml
steps:
    - uses: actions/checkout@v4

    - name: Save test data
      id: input_data
      run: |
       # something to generate an $input_data

    - uses: GuillaumeFalourd/stackspot-ai-rqc@main
      id: rqc
      with:
        CLIENT_ID: ${{ secrets.CLIENT_ID }}
        CLIENT_KEY: ${{ secrets.CLIENT_KEY }}
        CLIENT_REALM: ${{ secrets.CLIENT_REALM }}
        QC_SLUG: YOUR_REMOTE_QUICK_COMMAND_SLUG
        INPUT_DATA: ${{ steps.input_data.outputs.<OUTPUT_NAME> }}

    - name: Check Remote Quick Command answer
      run: echo ${{ toJSON(steps.rqc.outputs.rqc_answer) }}
```

## ▶️ Action Inputs

Field | Mandatory | Default Value | Observation
------------ | ------------  | ------------- | -------------
**CLIENT_ID** | YES | N/A | [StackSpot](https://stackspot.com/en/settings/access-token) Client ID.
**CLIENT_KEY** | YES | N/A |[StackSpot](https://stackspot.com/en/settings/access-token) Client KEY.
**CLIENT_REALM** | YES | N/A |[StackSpot](https://stackspot.com/en/settings/access-token) Client Realm.
**QC_SLUG** | YES | N/A | [StackSpot Remote Quick Command reference](https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc)
**INPUT_DATA** | YES | N/A | Data that will be received and analyzed by the remote quick command

## ▶️ Action Output

Field | Observation
------------  | -------------
**rqc_answer** | Can be accessed by using `${{ toJSON(steps.rqc.outputs.rqc_answer) }}`
