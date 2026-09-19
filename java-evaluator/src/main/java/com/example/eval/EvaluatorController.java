package com.example.eval;

import java.util.*;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.evaluation.FactCheckingEvaluator;
import org.springframework.ai.chat.evaluation.RelevancyEvaluator;
import org.springframework.ai.evaluation.EvaluationRequest;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/evaluate")
public class EvaluatorController {
 private final ChatClient chat;
 private final RelevancyEvaluator relevancy;
 private final FactCheckingEvaluator factuality;

 public EvaluatorController(ChatClient.Builder builder,
   org.springframework.ai.chat.model.ChatModel model){
   this.chat=builder.build();
   this.relevancy=RelevancyEvaluator.builder(model).build();
   this.factuality=FactCheckingEvaluator.builder(model).build();
 }

 public record Request(String question,String context,String response){}

 @PostMapping
 public Map<String,Object> evaluate(@RequestBody Request r){
   ChatResponse synthetic=chat.prompt().user(r.response()).call().chatResponse();
   EvaluationRequest er=new EvaluationRequest(r.question(),List.of(r.context()),synthetic);
   var rel=relevancy.evaluate(er);
   var fact=factuality.evaluate(er);
   return Map.of("relevant",rel.isPass(),"relevancy_feedback",String.valueOf(rel.getFeedback()),
                 "factual",fact.isPass(),"factuality_feedback",String.valueOf(fact.getFeedback()));
 }
}