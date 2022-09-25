Feature: Receive a webhook
    
    @test_01
    Scenario: receive a webhook
        Given a requestbin user creates a bin with the key 'stuart'
        When receive a webook with 'stuart' as key
        Then the request succeeded
        And the response body is as expected
