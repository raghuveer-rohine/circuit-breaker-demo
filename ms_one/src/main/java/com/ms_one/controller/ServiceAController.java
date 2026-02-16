package com.ms_one.controller;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/api/a")
public class ServiceAController {

    private final RestTemplate restTemplate;

    public ServiceAController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping("/call-b")
    @CircuitBreaker(name = "serviceB", fallbackMethod = "fallback")
    public String callServiceB() {
        return restTemplate.getForObject(
                "http://localhost:8081/api/b/data",
                String.class
        );
    }

    public String fallback(Throwable throwable) {
        System.out.println("Fallback method invoked");
        return "Fallback 🚑 | Circuit Breaker active";
    }
}

