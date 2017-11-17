#-*- coding: utf-8 -*-
__author__ = 'kinglee'

from selenium import webdriver
import time
import pandas
import re
import MySQLdb
from DB import HeroDB
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


driver=webdriver.Chrome()
 #职位和URI对照的字典
zhiweibiao={'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABaUlEQVR42mNgwA7SgNgUiV8OxEoMxAN7II4lRmERENtC2cuBOBzKlgbiL0DMg0VPIhDPxoIPAvE1HHJpyAYsRLII2dIuIH4MFUPGWUCsB8ReWPAEIN6CQ86AkKXyQPwBiP2waNZD0rsJagkMXwLi+2hi27AFLzZLdwNxLdTyHUAsiyNqPqHxk4F4CprYD2IsrYS6jgkqVgDE74DYEYelhHyK1VKQywKwxCky8IHGLxeSmCU0pQYg4SlQByOLgdSIY7OYDYpBhmsh8ZExH5qeLKglyHgvEF9BE7sLTQsoAJQl/gPxayjGx4ZlH0do/KHjhVCLkcXOQVO1G7qln3BE/A+0+ONBCtpwLHgmNOEhi50E4g6ksoBsSxmgrl+Iho8C8Q00sYe4gpccS62B2AUN90HzLrLYNiiNUgSuAeJfSCXOHxzsX1C1RWiO5oOm0HCoT3MIlbvGOIosfNgYzQxQfl4MdVgPjrIaDAC5foW6ShoocQAAAABJRU5ErkJggg==':'监事',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABdklEQVR42qWUMUgDQRBFDwsrsbGwEBEsLIJIOpEgIkgQK7tUV4iQIoiFnYi9hcgVQZBUYmEnInIIIQQLEUFSiIgIIiGlnVVKZ+EffL4TTnHhkezfnZ3d2b8XRX7bMIrUL0L7bVsy4rxJNaNBvBlN6jeh8ZwaNtJwuDVeBoxVs6RzxgqRGvvU3zUu8H/VKCMmsOaQGNcDxriC0R6S3RgfoGd8Gm0sErh0Sn1F44EnxLOWankLctKMAyzojRUo/kvW2zTqovU1aYxJSrjL5wFjsSTNO2nfM9OIcS7cw0Cqz1LcAjawTtRRTtbCnHFNOma0jGEi3N2xaCnKy87XKrScCr3DSD+S9sTebcf6XUq6jPtTTpGYtQ5cXf5v0lDaisMJXgFrDzDmot7pDn4zqliAtW1jhuISnIy5M15F63rlnccHgHnEXaheoriS85yOnKemXogmxGkZiePCjEnZ9CgcWsFJt/K+vVMI+AvTssaQcYYndYircNs3bFSWiVYudnIAAAAASUVORK5CYII=':'董事',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAOCAYAAAC2POVFAAAB/0lEQVR42rWVQUSDYRjHJ5MOiUw6TCJJJtltMpmYyQ7pNh12SOwwSbol6dClQ7LDRHaaDpEkySdmpkMS0yFJIpkOHbqlw+xSz5v/x9Pj+fZ+O/Tys33P+z7f+7zP+3+eLxDQxyIRZc9R2PyOBJH1sS5CFC1rgtKQJ0qMZ6LCniuw8TV5HKCkcEU8eszl2L5J4sMjyH6iTBzLiUk4ujjEJnteJ07xf5ZIwceQVigQFx5zUR/BLhHvxAkxoJ1kA0FeEq/gDS+rYXPDmSKJczZvuIc/tznKnjzYbtyWucEnHMxTO0mFHQSizUWY/6eSGanFZptg+4gvok4s2ISexcslRqsPHnNZEawts01LZoc6KOBAL3EkuMG1SPsE85tC4POMIq6d28yaQfiYwvnukD83FSKq0I6L0ea+sDnICO8kMutV5UZeFB3KAssiQdYRQkHxNlNTWlCDBTsDfUrKCJjb7tAlUm2C7cJ+uf8I1kggo3CArsJttyjYaUvrikHfSZtm1/DrksPG3LZCjDG/AjLJuUb74baGDxmME2EcrgWJqSOGxs+pQ2vSHmd+caWt7Sktz1Gy5QabwHyLfTTSmDPymeNOYVG5LgWlql1kq+lDgWSQ2WUfdbKKSjdBbSlfqxCKswUJ/Y5hbNQJI+LFpjgO0dp2IRnbGCW2iR7LOtPygj81EMiFCWOxNQAAAABJRU5ErkJggg==':'董事长',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAOCAYAAABevFBuAAAEC0lEQVR42r2YcUScYRzHXzknk8hkMnNkJjkTk5NkYjL3RyaSzEkikzmTyJzM/hhnTjInkiRJZDKZjHPOzElMf0xm4uTkTCIzk/tjtN/L95nv/fY819myh4973+d5n+d9nu/z+/2e33ueZy+jQgfdd6Cu1nJXiNX47C1hWNU1CFMX9LspPLLUx9FmK03CjPefyoSwSBwIGbrPoI6fmYDQixbeC58dbeNCQAiCkHAitFHdsvCa7oPow6VZKKkN6RGOhWuOdT4T1nD9UCg76FbGYfD7jAjfHZT4ZbeFe8Q2dtTcPxU2cX1f6EMfn6iFOeGto823+gQ2ylAU9nG9B2EyigTN14yVFF7QfUGYpXttpcfYRK+K6Hm69w0gDaEXsK4x1Jl5bOI6CGErSgJivhMOwRGsKAeRfN5YQsEWtft8Qn+u266ymDSFC56oq5wLG8K6gw08wyUlPMfifYEaVfsUvLHZ8r4ThCQPos5jnH7oEUR7hajtylINSQhma2un/nqHeDdNKav7ebiLz5lwiutT3JcIm6jBKqIHlagRCFYP48mq+L2M56cd42lRjcHsCl/JaCp0iEEETQZuaWuLKVEvstTyX1pq+RJEXcY4/jy/IQTUwb1LiPWdEGYfIa6aqDW7f4PFjXaww7o+TP26IMgDIo0Jcl2MDpA4JmPwY+FHXOexUNP2E7/TStRBNT4zqEStA1lkDGFYWB6HG5cBvN8PFa8g1Dl+DyGqOS9MDI4iFPwh6lW8lE/cUYofhm24P2cO2oqzFgsv0OFRj000LMBqGrCoLWor47f+H2NqQnlARM2BaQEuS/0irGCdRVyvukQ9UulPzpIaFUnUXrxEY17IdXs4PfvUyZqmkz8NKyhQm839o7A843Y7KsbXwVpN6YfFryFVW0ddyRHHX1Zx/wBtsA5VDZchqu/6QxYWkEVw3S4OPuNudzCpEQiXIpc6p9RoQ81zCRsSxQaYM+EAaZOHMOOL00r55hI8L4q16jNlvUqMZlHjpIXJlFifNh1TJ5UbjEMgrovjK8iUOVgmkycXMRQtuWMLYmleHVQ5bMKYev4KLCqkRPUQA0PwhCnMvUBCsxV3kaXXKuowQmEPGUoS82TjqfjwiKjDYxMLLljqu6lftyXdmrWkYjoW98C6eh2nfxMsIUvWPYk681zGIsA0Fu/B3WchYgpj/bDkzC5R/c35gNCRUx8gF+bU1x2n6JzlFDfcUGM0YnJDsLzHVXZ+BoK21ZBSjSMsJTB2F835DF5gXG8JX02d5H0BHH5PEHKMAfHX2j6yAa6Lw1MGKIaOKu/jg8rwO0sJqW/cWmi1uNUqdjxlC9pUQnBlU5IQzIM1r1jGDjj+jNHxPFzDfx1NsP5qtFr6hR2f3kzkF9n7lseFpaXKAAAAAElFTkSuQmCC':'董事长兼总经理',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACqElEQVR42r2WUYSUURTHx1irh8RKkqzoIVlj7dsaayWykmRfMg9ZSezDyDysXpL00EvWWvMwljWStTIkSdaItVZW1rL2IUkiWaOHLMk+jQx1Tn43Z447830zDx1+Zu65937f/d97zrlfJtNui8IR0x4Qqpl0dkWYyPRnt4Qx0x7Dl9YuCDNpBx8IR017UGilmHdC+C4UaK90QTeuyOYFPgvrpr2Oz44pIrwa4a3wsUPfbBqRzQSBOn5HWDa+QheywqhwyVAXHpj2PeEl/y8LU8wZJWI8ZWGtQ9+/CFlFzG9+n4P1NU1fsOPCO+EV7VM9hNh9xL0RvkKDjd5k0Ws824fua9OvvGe+9dXThOsAIg45UeU6OxzsEaJ17G1hN6XAEXeSgccIiPWNmPmH7nn67orzNdPmZE74YdrTTuSQOcEDCk+JF3aiRJGI9WkufujQN+NEJp1kV5G6Y+Psqi5o24msuTlZwusZ7ZjIFmEXRIZcrjm2KTjenzPvyyN42lAhPK1Px5z0JfgJ6rVK3mUx2t5KEFkjbytdwlOfM+l8mgobJhUGyb0l56sTrsGKkU3ciETAFwpPWxF4SBjYcF0yQocjIheEPfKyH5ENV+43I1fBvhF5kfzzrCDU+vaoulNJOamhcxUBWuKvkZNZ7sY8i63+J5H5DtfSMlXa+nZIucluIlXQNwTZrxoNn/MsMFg/IvU9c/wGZlmw9WnanDPzypEPDL3GPjnfvg9XL3KIQSXXr+J+cpW86EFkK/LJN05UWHbJJe+3cyci18ti5Orxufx3l28IvwjDLUInZg1OuJQgUqvtU17WoogEO+0qYaAcqZKBYff8Y1TQAid5J+lyvskRz9GeN3egtxwCB4yvRNWzNo/wMrlk7QwL7IWzkatrlUK44GpJm/0B+H4BqS3ysBwAAAAASUVORK5CYII=':'执行董事',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACg0lEQVR42rWXQWScQRTHR0SsWqGH6qFWyaGihypRqyKixB6qokJEVFWUVTlUDyGicqheqodaVbmsHKJiiYiIiBA5VA97yaGqclh66KGqQtUe6hNL+qZ+H5PJ++abrfbxY/b73nwz/5k3780ac9puCFWTbVV8NHsoXPKeTQvDJt4GhVHzn21KaATeN/DxrV84Fga853XEx9qSsBrhV2e8dga/8Dll94UjHBLaGgk+R/RJ7bGwR/urUPxLkW+FN5EiQ36zmsheJvZAWKetsY5PkT6ptYQx2m1P5IIwIdSE9zmT38M/RuQWY2rUNJFuuDbZJY2mEq4z7LBxRD5iV74J34U14YnQCUy8h+/sR4r8LGxk8CFPZItQ0Gh5Is8jJCHB2LNwwrmySWfHCdeCtxi+jdL/p3AhIkFdCbwv4fNPEs8KghKST1EJ11Rk+i7Lanx/WZgP+N0lIpIcOhlJ8s/DThcdnwsXlXDVRF4jKZmM7Gz7VYSbREchIHJbKW1+6dkIiey2hPRFiNwUPrHzmr0QDp3fTRYwVuQquSEossqZ2404k7u0Z7sQeUcYF4bIzq6ViZCK8mw4UuSOsvhnRI4xmZR5hKe/54Snnk8lQuSSt8J20HfO78uEppYJXwk/WJiQyBIXgwPm1ZcXrvZsLJLhprwycUy4jkSE60AgLJdpD3FG952JGWWH2t7Fo8ep0WVKiV3MW0SZXZiXLOCZkEmvSrbgX1UGtAnmGbedj4SfJrLB+VrxWOP7ZRatw2oXAjmgl3p7wiXBjnWbjThgARaU8lJ3NuW6u1O1nNpjnHo3xy0mncim935SuUhMO98v5fwR8G2ccezZ/kKiuSecy6mVr+24vwGFkdkzltO0vAAAAABJRU5ErkJggg==':'其他人员',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACk0lEQVR42rWWQWRcURSGn4roYoSI6qKqVESMitlVRUSJqCxidhExiwgjYlR1U1XVRZUsqkY9pSIisggREREjjIgsIsLoIqqqVEXULGYXXTxPaM+p/9bpce6dN6WXz9x37rtzz3/vOee+KOq8dREznrFZoiCeC7BlbaNEKcN7eSLO4OdfbYW4CPBWvJsjEvQXiCXBF6IunuuwyXcWIHzJ4JD45BkrCx/GiJZHXC+xSmz8wwFGW0RRiRzCgo4a8Vw8P8U87j8gxjGHmTCoEruesUIGkXNEk9gkrlkiFvHCd0ETdp9Ibs8gbo/4Bs7hxAGcZraN0N0R48wp5ktbzfBViuxGdHDEfMaGeFuMndA7EwdE5tVJOhYhwBrLi/+/CKznWhIQ2UP8IBrEdJZwjJETOkdCIksY13AufvSMlZTIdieZtDnJm53kHC9eUXlQEU75wpWf1xXHCB9tvyPm3cN/FwUxwlPa+J3rmMMF5WeH/ImMq/gDH7mAyD5iH7nh4Nx7p2w1nEAkKrM+5X0jAr4aeaYLTwkbG2w5hI7Lm1T0GxASEnmuwvzAuArOhMj7yD/NKoRK2wdU3fGAyCtYr5xF5AhIRf/kP4jkUJ0yeI8qLW0nKGQjba6Qu/BrLCQyEblzKfpNCBnC3WPl5GP8OspwWNoeEgNiXtVIiyNcA9J2liFcB4kb2JQUqWCKbHnKdh0i5RdFonZwS9FALmn7sJg3bFwvb4yrp2acjhM5ivFUfCxMYIzDfNI6SVe2L0W/BZFPUAj2ICDC7hUNqkaVdOiS34PCMYWTrGS4CR6hcrJvL4yvmz74moqPmd/VdV1VQ8crbMI8sYz8crt2Cw52wm3lEBeNNaz/Gmu1a/3ES/gdanz1dP0CG38SpdFXf2kAAAAASUVORK5CYII=': '副董事长',


    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABoUlEQVR42r2UT0REURTGr5G0eCJJWkWrFrNLxshom1m0mM1IRkak1WgRLUbSLmmRJDIyRtImaTFGJC3Sov0s0ma0GEkkSVrE9J18L2fuvDtv2nT5effdd+89/77zjGkefWDV/PNYA0ecz4JPBxPcMwkyCjkzB94c1E1AlE9gOMSpG/W+AHbpyD7YBvNck5EEp5x303DT2ALr/CgX9Frfl8E9GAhw5hl4nIvRPd4zDc4492yjMV7YA/LgUn2TzUXQACuODNhGa6AMbsEj5xXbaJEpksVXpjjC9EkdCmCcB6tgKsRoR+mNEIlwEUTpodQvYRlI0REpxQ4vavBZo9EyDfoaSDLVLTXNK6/8lHsOhogr0jtQYhAPnB/aRsWLL7bLCTjmWp28gA/1vtkmvV3Uhp1eo/b89tsByHJjv3Vpho6YDoSUowaEc6a8oBgNukBqG+fzL0Zn2CqigTTZoILTikH/UJx9KjV4p0o7iVR695qluaIu9LDT26LIJTCmRHShqFLNei1H0aRUDbMUTSlASD6uXv/5JSZCGAk4F2V07Yh9A2Qgg+AVrBiLAAAAAElFTkSuQmCC': '经理',

     'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAOCAYAAAC2POVFAAACPUlEQVR42sWVX2SVYRzHHzNHcsSRJF2MyWR2l5kk3SXnYjKOYzKZMV0dk9jFJF3EZCZJzMwcSczMLmZipovM7H4XGZkuJhlJki5ifX983vl59j7vToz9+DjP8573eZ7fn+/ze0M4alfEg5znDf7Ls4p4HE7BLog9Meie3RTfxMXEmifiLeN74k+CG7xzSww5bM198TPBXt6hVZgUz9z8s5h28zirFkhHQQIsmA03HxWvCGBGvBAjPMv8WGJcwuEjdiAWxLsEC7zjbUo8ZVM7+Fz0/yOxQ8Vi2xdlxubsa/bpF8uMy0XOlgoyVIqc7cORM2JCrLv/7JB53h9P7Bc7uytWxJb4ynj1pJydp5S22Q+k0EaZTWezopcDt8WdY5z9bxnUxN0EtcjZNling/SQkQ0upbcBAjDJvMSBA353cXYFRzONV5HEiWl2wmUhk0Y5wSVIZfaTaBL8F8ZvUs5WyVSW/k3RHWWy5uYW9V/a1iIB9ZNB47v47ebPC2TQjvZjGQT3zqHNobUq5Qj0wB3aU6DP2qGdrl/aumHWnY/2HCKA0MIFa6Bx4z3SmHVczRadJQMdkbMBjdnz27ShUfpuJTrYsn7dVaZVZwdpWabxOkzSEeqOww/SQ6LJSrCWs/E4mwbKPo1zU2jsF7e+lcxa0B+R0Ad0H8txKRVhnYPNLpPlpivBHF+pXqehdm74mLjmLteaY5vu4J81uEwDTqPDnNfMuWAZqV4duqIS1GlLx1mFchbRmbOux33KU/T9A1cGuQIA/VG9AAAAAElFTkSuQmCC':'总经理',

    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACxUlEQVR42r2WX2RbURzHr4iYiRE1NXsoNTNTM6aqpvYyM3moKRFVNVWqDxMzIw8104dSUzVTY6aiZkJN7KGmVE1NTdljH6bM7CFiwkzNTIXtd/hcvjnuvUkfusOHc07uPff3/f07CYLjj7QxEbF/wZiN2C/xW9TIGY+C/zQqxmECz+TZrPEn4oyzRt0Yl70R47vRG/Pdx8Zr5hOcG8V1nrlhTArunbsJdteP64iacSdGZB4WjQVZfzGWZe1H0TmgL+Gbzgm7sp4xVvj+C+OpMc1eaEeNeQahbcMZ2EB9SIP9TiL/GutGNYZ1ntGxZMxjjDP4jPf7Q+OADPFHEzsCRD7nnFHjLfNslMgVXtChXuokMpMQkYwncggBp4w5Y9srhwrPl2PO80V+NTaMPQLj5u/iRO4YL4WdExJZ4QxnxE9SNkU61vn2IIbuG7c7iOw6XV0h35P6ybOe7FJkgd+jKHgiU7BNRx4gArs0Kx1jCJ+nAR5y1iERnCZyeanhPKnbJtKlzVoC2ROoyTnxepjC2RjOQVwkP2Onc9o35q98kWGR3oQjmX8yerrorilJk4/GZS9yBVk7L7e4Pt7giFFpeD+M37J+kpCuaYLkp2sgz7SJHIEjme91ELlKLeVJmzD1D7gmAu5JZ2y/3HfuvSne64konWpCjavIkvSQTVJY+8ol/4IP06sl8wZGXKGdq8jTeLzPExlQQ27/FtfBDPdmzjPYRXlYMqFbkeNcHS4QRVgkKEWhV0U25RCN1Jbn6Zz8/gDvhamyFWFQGWMC0nMZUUvU0C+6aDeRdM76QBDeU9d+2dTiPBNGZwNaMm8iskyr3iQiAZ4aZn6eqK5Jqqzyr2ZQvpOmY943rknT2RL2ySDdK9FkxqQGp7wGqY0npKzdtUrT8FnAuFmMdsZfjXHWRS9VilwPnUZOekAc/RHvDXhXXhRD/wB5SwMiRVOUpAAAAABJRU5ErkJggg==': '副总经理'
     }


# url='http://www.gsxt.gov.cn/%7Bbnra9gd-l_k2K9GqiZCu-R6tyu4M8DDmxgzx4rm7AIKu0rQyb6HUcboOdwFsGgip2OaC2faKFENjAMYZZRw4ovBzAz_2lnqmvOopGG3-9c17Eg9n-OCo_-vW1mbq0rMh-1504666644532%7D'
url=['http://www.gsxt.gov.cn/%7BBIpUiz2ySe_d1Zd8nSikrFMeQFGfCJEpu1v92i6rnuPLauFNB0zqm6u9-5GX80x8K4tn2F9mmb-NIl--ZwPcntqWqaRR57CYjOm8e8VtB0b3jjw-bhuRV8jlugCFom1Y-1508981306646%7D','http://www.gsxt.gov.cn/%7BBIpUiz2ySe_d1Zd8nSikrFMeQFGfCJEpu1v92i6rnuPLauFNB0zqm6u9-5GX80x8x71nWLX87Dkz_ULWZsEOUxht9ownoVoxXdGYk7wUXT9t5xL3E8G8oHgD58yz0PUK-1508980989967%7D','http://www.gsxt.gov.cn/%7BEbmYKfydJwF7l8fh4Qrhps_bRETdJbnBBrANWwfUazs8qT-ktLLkHuBjoem9TtvW-nHuDLjaAN3InjmS5ZUZcVXr8NO2MssNNI5JItpnqTl44E7Gk-_5DFIsFeG5CAZT-1508978450538%7D','http://www.gsxt.gov.cn/%7BhAmmc6FpT8V618uMFjSZmqZcgLK7nzGI2PudIqVDgJ9Hwk5dLczBIYPEv87WfIch4_zfynyKGKt0XEDe9KfKx6lH-yxyr0ZyqJ3AwDg9J1pcmau5rbjdh20kPVHkPY28BJp_A5mlO3-rzLC_VTlqSg-1508980306677%7D','http://www.gsxt.gov.cn/%7BpaXLVyWEb_ViKy3-BtzuXnnnvN-1FAyyyTVkPXJ-z5tDV7PJCkUxk1UE4q1Wc6jLTnJDL18SDeoPrHfLpCoaat6DDq-4-Wfu__ZiB8RfkgRAhN8ou6djL7PvONVMM3Nb-1508979729301%7D','http://www.gsxt.gov.cn/%7BQ1DaO6xsy2U8dBKR7Zzr35bGwYbe4fnx7k3NScI6lLCDnyd-NtiO9MbOGEst11aS6YtNBFbd-1fbzvhfyWYjjZ-McqD7hdELPz-7oIkRE95akzP7c_E04OZ2KBzfJrM5-1508977256932%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LCOAYuIAC9ArYAntsgnI3C_eqPGxSTxfh5VAGkPjgogDJJMf2hZZtnvaCr2lHA6fg-1508917426272%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9L2kY2Z_ctnD1_GvkL44LizEyywsY8Fp0C4UNY2qy1Acgntid26AaMo1pCeHgKDUug-1508918591065%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9L0_4Z7-knQrlkWfTYlZk64C_dhrKag9ZO0NqAlMYiuNuUJtpJIaplLoi_-JjY-_fWfQtfn5t-wFY5MPO4dhLulA-1508918591067%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LhTO5ZQuj0WIMKPEhZ6M6-MqUr97ld8vC7zdrAI4J1FXR1zpZcFgrEvfmjOzaMzlx4Uv-VnP5mShl_YIUIUzV-2PW9ED6N7DGn9TjS2-VRGQ-1508918591063%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MkWCUBHgLcr7xDLUf7diFsRBJHhLUiSfiB9gA_8TB3MT-1508911915425%7D']
def Key_person_info(url):
    Con_info=[]
    for j in range(len(url)):
        person={}
        Rzhiwei={}
        driver.get(url[j])
        if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
            pass
        else:

            time.sleep(10)



            #下拉加载处理
            driver.execute_script('window.scrollBy(0,3000)')
            driver.execute_script('window.scrollBy(0,5000)')
            driver.execute_script("window.scrollBy(500,0)")
            time.sleep(5)




            #获取所有主要人员名单
            try:
                driver.find_element_by_xpath('//*[@id="keyperForAll"]/span/a[2]').click()
                #切换到最后一个句柄
                driver.switch_to_window(driver.window_handles[-1])
                print 'ok'
                driver.find_element_by_xpath(' //*[@id="more"]/a/span').click()
            except:
                pass
            for i in range(1,30):
                try:
                    person[i]=driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[1]' %i).text
                    person[i]=''.join(re.findall(ur'[\u4e00-\u9fa5]',person[i],re.M))
                    # print person[i]
                except:
                   break
            #在下次的循环里如果没有新开句柄，就会把driver关掉，所以不能这么写，应该先判断一下是不是只有一个句柄
            ##在driver.find_element_by_id("").click()之前加上
            # driver.switch_to_window(driver.window_handles[-1])
            #
            # 或者先用driver.current_window_handle拿到开始的handle，然后遍历window_handles,如果不是开始的handle，再switch
            # #关闭最后一个句柄
            # driver.close()
            #切换到第一个句柄

            ##一人多个职位，返回字典会用新读取的覆盖掉前面的，下面是给重名加符号，不会被覆盖，可以正确显示所有职位信息
            for i in range(1, len(person) + 1):
                for j in range(i, len(person) + 1):
                    if person.get(i) == person.get(j + 1):
                        person[j + 1] = person[j + 1] + str(j)
            #print person
            time.sleep(1)
            #把person的value付给职位表的key
            # for i in range(1,20):
            #     try:
            #         Rzhiwei[person[i]]= zhiweibiao[str(driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span/img' %i).get_attribute('src'))]
            #     except:
            #         try:
            #             Rzhiwei[person[i]]=driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span' %i).text
            #         except:
            #             try:
            #                 if driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[1]' %i).text:
            #                     Rzhiwei[person[i]]='空'
            #             except:
            #                 break
            #     # print Rzhiwei[person[i]]
            #
            # #获得人员和职位的对应字典
            # #print Rzhiwei
            #
            # #把字典追加进里表中，得到返回的json格式字符串
            # m_people.append(Rzhiwei)
            # print m_people
            # #输出到excel直观观察
            # P_result = pd.DataFrame(m_people)
            #
            # P_result.to_excel('Person_he.xlsx')
            #
            # print m_people

        #职位分开来
            for i in range(1,30):
                try:
                    Rzhiwei[i]= zhiweibiao[str(driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span/img' %i).get_attribute('src'))]
                except:
                    try:
                        Rzhiwei[i]=driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span' %i).text
                    except:
                        try:
                            if driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[1]' %i).text:
                                Rzhiwei[i]='空'
                        except:
                            break
            if driver.window_handles[-1]!=driver.window_handles[0]:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
            else:
                pass

            #该公司社会统一编码
            scocial_Code=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
            #把信息整合成字典的形式，加上社会统一编码

            for i  in  range(1,len(Rzhiwei)+1):
                result = {}
                result['name']=person[i]
                result['position']=Rzhiwei[i]
                result['social_unique_code']=scocial_Code
                Con_info.append(result)

    print Con_info
    print len(Con_info)


    return  Con_info


Con_info1=Key_person_info(url)
res=pandas.DataFrame(Con_info1)
res.to_csv('kpit.csv')

# #取出每个字典中的值,insert用,主要人员
# data=[]
# for i in range(len(Con_info1)):
#     try:
#         data.append(Con_info1[i].values())
#     except:
#         break
#
#
# conn = MySQLdb.connect(host='192.168.60.100', user='root', passwd='ahzx2016', db='test1', port=3306, charset='utf8')
# cur = conn.cursor()
# db=HeroDB('hello', conn, cur)
#
#
#
#
# # db.createTable_v('hello2',{1:'name',2:'position',3:'social_code'})
# db.insertMore('hello2', data)
# #查询
# #db.select_p('hello2',['name'])
#
#
#
driver.close()

