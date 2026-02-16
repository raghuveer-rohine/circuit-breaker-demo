package com.ms_two.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/b")
public class ServiceBController {

    private boolean fail = false;

    @GetMapping("/toggle-failure")
    public String toggleFailure() {
        fail = !fail;
        return "Failure mode: " + fail;
    }

    @GetMapping("/data")
    public String getData() {
        if (fail) {
            throw new RuntimeException("ms-b is DOWN!");
        }
        return "Response from ms-b ✅";
    }
}

