package cn.crowdos.kernel.controller;

import cn.crowdos.kernel.CrowdKernel;
import cn.crowdos.kernel.Kernel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

@Controller

public class StartController {
    @Autowired
    CrowdKernel kernel;
    void start(){
        kernel = Kernel.getKernel();
        kernel.initial();
        System.out.print(kernel.isInitialed());
    }

}
