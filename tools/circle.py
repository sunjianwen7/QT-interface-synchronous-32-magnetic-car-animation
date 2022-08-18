
from numpy import mean, sqrt, cos, linspace, pi, sin
from scipy import optimize
from matplotlib import pyplot as p
from sympy import solve, Symbol


class Arc_Fitting():
    def __init__(self):
        self.result_symbal=0
    def full_data(self,x,y):
        self.x=x
        self.y=y
        print("input data ",x,'\n',y)
    def __calc_R(self,xc, yc):
        return sqrt((self.x - xc) ** 2 + (self.y - yc) ** 2)
    def __f_2(self,c):
        Ri = self.__calc_R(*c)
        return Ri - Ri.mean()
    def Calculate_Circle(self):
        x_m = mean(self.x)
        y_m = mean(self.y)
        center_estimate = x_m, y_m
        center_2, _ = optimize.leastsq(self.__f_2, center_estimate)
        xc_2, yc_2 = center_2
        Ri_2= self.__calc_R(xc_2, yc_2)
        R_2= Ri_2.mean()
        self.xr=xc_2
        self.yr=yc_2
        self.r=R_2
        if self.yr<=self.y[0]:
            self.result_symbal=1
        else:
            self.result_symbal=-1
        return self.xr,self.yr,self.r
    def Calculate_points(self,x_list,a,b,r):
        x = Symbol('x')
        y = Symbol('y')
        func = (x - a) ** 2 + (y - b) ** 2 - r ** 2
        x_and_y_list = []
        self.result_symbal = 1
        for i in x_list:
            result = solve([func, x - i], [x, y])
            if self.result_symbal==1:
                if result[0][1]>=result[1][1]:
                    x_and_y_list.append(result[0])
                else:
                    x_and_y_list.append(result[1])
            elif self.result_symbal==-1:
                if result[0][1]>=result[1][1]:
                    x_and_y_list.append(result[1])
                else:
                    x_and_y_list.append(result[0])
        return x_and_y_list



    def plot_all(self):
        p.figure(facecolor='white')
        p.axis('equal')
        theta_fit = linspace(-pi, pi, 180)
        x_fit2 = self.xr +self.r * cos(theta_fit)
        y_fit2 = self.yr+self.r * sin(theta_fit)
        p.plot(x_fit2, y_fit2, 'k--', lw=2)
        p.plot([self.xr], [self.yr], 'gD', mec='r', mew=1)
        p.xlabel('x')
        p.ylabel('y')
        p.plot(self.x, self.y, 'ro', label='data', ms=8, mec='b', mew=1)
        p.legend(loc='best', labelspacing=0.1)
        p.title('Least Squares Circle')
        p.show()


if __name__ == '__main__':

    x = [36, 36, 19, 18, 33, 26]
    y = [14, 10, 28, 31, 18, 26]
    arc=Arc_Fitting()
    arc.full_data(x,y)
    arc.Calculate_Circle()
    print(arc.Calculate_points([27]))
    arc.plot_all()