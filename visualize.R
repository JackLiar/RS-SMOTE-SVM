rm(list = ls())
load("./original.RData")
# chol <- read.table(url("http://assets.datacamp.com/blog_assets/chol.txt"), header = TRUE)

library(ggplot2)
library(ggmosaic)
library(Cairo)
library(showtext)
library(vcd)
# library(NHANES)

showtext.auto()

# Histogram figures
pdf("Age_Histogram.pdf")
qplot(cdata$Age[cdata$Client_Category=="逾期"], geom="histogram", binwidth = 0.5, main = "Histogram for Age",
      xlab = "Age", fill=I("black"), col=I("red"), alpha = I(1), xlim=c(25,52))
dev.off()

ggplot(data = NHANES) +
    geom_mosaic(aes(weight = Weight, x = product(SleepHrsNight), fill=factor(SleepHrsNight)), na.rm=TRUE) +
    labs(x="Hours of sleep a night ", title='f(SleepHrsNight)') + guides(fill=guide_legend(title = "SleepHrsNight", reverse = TRUE))

# fill：纵轴类别划分及马赛克块填色规则
# x：横轴长短的比例来源
# weight：纵轴长短来源,必须是数值型变量
cairo_pdf("D:/Documents/毕业设计/Paper/figures/Age_Mosaic.pdf",
          width = 6.7180120833334, height = 7.08661417 )
ggplot(data = cdata) +
    geom_mosaic(aes(weight = Loan_Amount, x = product(Client_Category),
                    fill=factor(Way_of_Mortgage)), na.rm=TRUE) +
    labs(x="客户类型（从未违约/逾期1月以内及时还款/逾期1月以上）") + 
    guides(fill=guide_legend(title = "年龄", reverse = TRUE))
dev.off()

vcd::mosaic(table(factor(cdata$Client_Category), factor(cdata$Age),factor(cdata$Way_of_Mortgage)),
            main = "Survival on the Titanic", shade = TRUE, legend = TRUE)
