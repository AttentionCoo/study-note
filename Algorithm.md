# 方法

## 1. 图的邻接表存储

![image-20250122222614968](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250122222614968.png)

#include<bits/stdc++.h>
using namespace std;

const int maxn=100000+15;
int n,m,sum,tot;
int head[maxn],ru[maxn],ts[maxn],dp[maxn];
struct EDGE
{
	int to;int next;
}edge[maxn<<2];
**void add(int x,int y)**
**{**
	**edge[++sum].next=head[x];**
	**edge[sum].to=y;**
	**head[x]=sum;**
**}</u>**

![image-20250122230822221](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250122230822221.png)

### 样例

void topsort()
{
	queue <int> q;
	for (int i=1;i<=n;i++)
	if (ru[i]==0) {
	q.push(i);
	ts[++tot]=i;
}
	while (!q.empty())
	{
		int u=q.front();q.pop();
		for (int i=head[u];i;i=edge[i].next)
		{
			int v=edge[i].to;
			ru[v]--;
			if (ru[v]==0) {
			q.push(v);ts[++tot]=v;
		}
		}
	}
}
int main()
{
	scanf("%d%d",&n,&m);
	for (int i=1;i<=m;i++)
	{
		int u,v;
		scanf("%d%d",&u,&v);
		add(u,v);
		ru[v]++;
	}
	topsort();
	for (int i=1;i<=n;i++) dp[i]=1;
	for (int i=1;i<=n;i++)
	{
		int u=ts[i];
		**for (int j=head[u];j;j=edge[j].next)**
		**{**
			**int v=edge[j].to;**
			**dp[v]=max(dp[v],dp[u]+1);**
		}**
	}
	for (int i=1;i<=n;i++)
	printf("%d\n",dp[i]);
	return 0;
}



























## **2. 树链剖分法**

针对问题：

![image-20250127233514658](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127233514658.png)

![Screenshot_20250127_234827_com.deepseek.chat](C:\Users\hp\Downloads/Screenshot_20250127_234827_com.deepseek.chat.jpg)

dfs序作用：

![image-20250127233852110](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127233852110.png)

![image-20250127234346830](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127234346830.png)

### dfs序

![image-20250127234733565](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127234733565.png)

![image-20250127235124457](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127235124457.png)

![image-20250127235214465](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127235214465.png)

![image-20250127235334033](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127235334033.png)

![image-20250127235804523](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250127235804523.png)

![image-20250128000200245](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128000200245.png)

![image-20250128000543613](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128000543613.png)

![image-20250128000954915](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128000954915.png)

![image-20250128001312368](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128001312368.png)

![image-20250128001645320](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128001645320.png)

![image-20250128001720963](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128001720963.png)

![image-20250128001745929](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250128001745929.png)

### ST表

![Screenshot_20250128_150602_com.deepseek.chat](C:\Users\hp\Downloads/Screenshot_20250128_150602_com.deepseek.chat.jpg)

### 三者关系

![89efc8e0e72c3988ea4d422a8bfdd326_720](C:\Users\hp\Documents\Tencent Files\1759751014\nt_qq\nt_data\Pic\2025-01\Thumb\89efc8e0e72c3988ea4d422a8bfdd326_720.jpg)







## **3. LCA模板题**

![image-20250129180024269](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250129180024269.png)

第一表示以j（j是时间戳）为一个标尺的一个范围的时间戳最小的一个爹。

第二是比较两个节点时间戳的大小。

第三是把它赋值为爹。









## **4.线段树**

**其实就是ans(也是t)是一棵装在数组的树，build不断把问题给的区间二分，好装进这棵树**

![image-20250204145647450](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204145647450.png)

对结合律的解释
![image-20250204145715869](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204145715869.png)





## 5.数论中的欧拉定理

![image-20250410165600048](../AppData/Roaming/Typora/typora-user-images/image-20250410165600048.png)

![image-20250410165632375](../AppData/Roaming/Typora/typora-user-images/image-20250410165632375.png)



**互质的定义是两个数的最大公约数为1**



### 配套取模性质

**模运算的保传性**：
模运算有如下性质：如果 x≡y(moda)x \equiv y \pmod{a}x≡y(moda)，那么对于任意整数 iii，有

ix≡iy(moda),i^{x} \equiv i^{y} \pmod{a},ix≡iy(moda),

在适当的条件下（比如指数运算结合多次乘法时，这种“降模”是允许的）。
因此，在指数塔的每一层，只要我们知道上层结果 xxx 模 aaa 的值，那么用这个值计算 ixmod  ai^x \mod aixmoda 与用真实的 xxx 计算再取模是等效的。

![image-20250211171337249](../AppData/Roaming/Typora/typora-user-images/image-20250211171337249.png)





## 6.快速幂最快写法

int quick(int base, int x, int mod){
    int res = 1;
    while(x){
        if(x & 1) res = res * base % mod;
        base = base * base % mod;
        x >>= 1;
    }
    return res;
}





## 7.求最大公约数

gcd(a,b)函数

















## 8.数组减法

**关键点borrow，负数直接对结果取反**

void subtract(int* A, int* B, int len) {

  borrow = 0;

  for (int i = 0; i < len; i++) {

​    int diff = A[i] - B[i] - borrow;

​    if (diff < 0) {

​      diff += 10;

​      borrow = 1;

​    } else {

​      borrow = 0;

​    }

​    result[i] = diff;

  }

}

## 9.取绝对值

#include <iostream>
#include <cstdlib> // 用于整数的绝对值
#include <cmath>   // 用于浮点数的绝对值

int main() {
    int num1 = -10;
    double num2 = -10.5;

    // 计算整数的绝对值
    int abs_num1 = std::abs(num1);
    std::cout << "整数的绝对值: " << abs_num1 << std::endl;
    
    // 计算浮点数的绝对值
    double abs_num2 = std::abs(num2);
    std::cout << "浮点数的绝对值: " << abs_num2 << std::endl;
    
    return 0;
}

## 10.关于大数的乘法

![image-20250408221114668](../AppData/Roaming/Typora/typora-user-images/image-20250408221114668.png)

![image-20250408221140669](../AppData/Roaming/Typora/typora-user-images/image-20250408221140669.png)

![image-20250408221159506](../AppData/Roaming/Typora/typora-user-images/image-20250408221159506.png)



## 11.除以某个数后取模

**注意只能减2！**

![image-20250409224053956](../AppData/Roaming/Typora/typora-user-images/image-20250409224053956.png)





条件

![image-20250409225840409](../AppData/Roaming/Typora/typora-user-images/image-20250409225840409.png)

计算

![image-20250409225721156](../AppData/Roaming/Typora/typora-user-images/image-20250409225721156.png)

## 12.乘法逆元

### 欧几里得扩展

要求a和p互质

![image-20250721115604376](../AppData/Roaming/Typora/typora-user-images/image-20250721115604376.png)

![image-20250721120116161](../AppData/Roaming/Typora/typora-user-images/image-20250721120116161.png)

### 线性逆元

![image-20250721123357753](../AppData/Roaming/Typora/typora-user-images/image-20250721123357753.png)

## 13.素数筛

时间复杂度O(n)

primes = empty list
for i in [2..n]:
    if not vis[i]:
        primes.append(i)
        // 这里可以做一些“i 是素数时”的额外操作
    for p in primes:
        if i * p > n: break
        vis[i*p] = true
        // 这里可以做一些“i*p 是合数时”的额外操作
        if i % p == 0:
            break

## 14.最小公倍数定理

![image-20250721140604497](../AppData/Roaming/Typora/typora-user-images/image-20250721140604497.png)













# 千万注意要审题



## 1.最好把要表达的意思全部写上，不省略

## 2.千万别急得做得很快，也不要一直死磕一道题！！！

# 经验

## 1.数据范围只有50以下的题，一般dfs。数据范围4000左右的题，一般二分

## 2.巧设数组

    // row[i][d]：第 i 行上数字 d（0 表示 '1'，…，8 表示 '9'）是否已被使用
    // col[j][d]：第 j 列上数字 d 是否已被使用
    // box[b][d]：第 b 个 3×3 宫格里数字 d 是否已被使用











# 动态规划

## 1.在字符串中的应用

通常是dp[i]表示字符串s[0....i-1]

## 2.动态规划的一些适用情况

动态规划的题目分为两大类，一种是求最优解类，典型问题是背包问题，另一种就是计数类，比如这里的统计方案数的问题，它们都存在一定的递推性质。前者的递推性质还有一个名字，叫做 「最优子结构」 ——即当前问题的最优解取决于子问题的最优解，后者类似，当前问题的方案数取决于子问题的方案数。所以在遇到求方案数的问题时，我们可以往动态规划的方向考虑。

## 3.无后效性

![image-20250706212100131](../AppData/Roaming/Typora/typora-user-images/image-20250706212100131.png)

## 4.无后效性深刻理解

**注意：一定要是前置条件已经解决，所以从左往右推**

![image-20250706212301759](../AppData/Roaming/Typora/typora-user-images/image-20250706212301759.png)

## 5.难点

怎么设计状态

## 6.记忆化搜索

适用于无后效性顺序不好用for循环枚举的问题

![image-20250706213158515](../AppData/Roaming/Typora/typora-user-images/image-20250706213158515.png)

## 7.其实有两种考虑，顺推和逆推

顺推是到哪里去

逆推是从何而来。逆推中有拓扑搜索，其实和拓扑排序一样

## 8.有些题可以考虑升维

一维数组不行，就开二维，第二位存某些题目上的值

## 9.避免记忆化搜索的方法

其实也有搜索的影子

**就是利用题目，巧妙地设计状态，一般可以浓缩题目状态（要题目碰巧才行）**

![image-20250831000419530](../AppData/Roaming/Typora/typora-user-images/image-20250831000419530.png)











# 解题思想

## 1.注意这里的自然思想

其实就是想明白每个变量表示的意思，以及它与其他东西的等量关系

![image-20250505191325367](../AppData/Roaming/Typora/typora-user-images/image-20250505191325367.png)

## 2.模拟题目，看看有没有什么数学性质

并且思考是否可以逆向

## 3.递归的三种看法

1.每层只解决小部分，大部分问题往后抛

2.明白整个函数的意义，按照这个设计

3.感觉递归是一种规则，就是对每一个传入对象应用这种规则

## 4.所有题的终极思想：顺不行，就逆！

为什么有这样的思想，我是从图得出来的。搜索时，一个节点有很多个后继，但所有后继只有一个前驱，这样可以巧妙存储一条路径。这种解法是数学终极思想的映射！

## 5.对dfs的一些想法

**dfs适用于对目标序列数量一定会变化并要从中找出符合条件的特殊处理**

dfs可以排序

**dfs优势在于可以回溯**

## 6.二分方法（用这个）

![image-20250806113036162](../AppData/Roaming/Typora/typora-user-images/image-20250806113036162.png)







# 线段树想法

## 1.

对于线段树他的优化是不关注某些具体的个体的细节，而关注与他相关的区间的整体，这也是它的优势，他的整体时间复杂度才降低，所以对于某个个体并不现实。



## 2.

l,r 任务范围，tl，tr当前来到范围



## 3.

懒信息就是要懒，必须要往下传时，才传



## 4.

流程：

1.先看要更新的任务范围是否包含来到范围

2.是，懒标记与新标记运算然后加在该节点上

3.否，下传懒标记





## 5.query数组也要下传

![image-20250515102342016](../AppData/Roaming/Typora/typora-user-images/image-20250515102342016.png)

## 6.关于懒标记

### 先修改该节点，再下传懒标记

懒标记是子节点该加的值，不是本节点

### 懒信息只下发一层，并且是该节点所包含的部分区间有修改才下传，否则只修改该节点，不改懒标记

![image-20250515093751815](../AppData/Roaming/Typora/typora-user-images/image-20250515093751815.png)



### 结束后的懒标记

在标准的线段树实现中，**不是所有懒标记最终都会被自动清除**。它们的清除与否取决于后续的操作是否“触及”到它们所在的节点。理解这一点对掌握线段树的工作原理至关重要。

以下是详细的解释：

1.  **懒标记的清除时机：**
    *   懒标记的清除（或者说“下传”、“应用”）**不是**一个后台自动发生的全局过程。
    *   清除只发生在**后续操作（查询或更新）需要访问该节点的子节点时**。
    *   当代码遍历到一个节点（比如 `node`），并且需要进一步访问它的左孩子（`2 * node + 1`）或右孩子（`2 * node + 2`）时：
        *   它会**检查**当前节点 `node` 是否有未处理的懒标记（`lazy[node] != 0` 或对应的无效值）。
        *   如果有，它会**执行下传操作**：
            *   将标记的值应用到当前节点的数据（`tree[node] += lazy[node] * (区间长度)` 或对应操作）。
            *   将标记的值**累加**到左孩子和右孩子的懒标记上（`lazy[left] += lazy[node]`, `lazy[right] += lazy[node]` 或对应操作）。
            *   **清除**当前节点的懒标记（`lazy[node] = 0` 或对应无效值）。
    *   这个下传操作通常封装在一个 `push_down(node, left, right)` 或类似的辅助函数中，并在递归进入子节点之前调用。

2.  **为什么不是所有标记都会被清除？**
    *   **未被访问的节点：** 如果一个节点拥有懒标记，但在程序后续运行的生命周期中，**没有任何查询或更新操作需要访问它或者它的任何后代节点**，那么这个节点上的懒标记就**永远不会被清除**。
    *   **设计哲学：** 懒标记的核心思想就是**延迟更新**。只在实际需要数据时才进行更新操作。对于那些永远不再被访问的节点（或者子树），它们上面挂着的懒标记自然也就没有必要被清除，因为相关的数据（可能）已经不再需要。强制清除所有懒标记是低效且违背懒加载原则的。

3.  **这对正确性有影响吗？**
    *   **没有影响。** 这是线段树懒标记机制的正常行为，**不会影响线段树操作的正确性**。
    *   **查询：** 当执行一个查询操作时，它只会访问查询区间覆盖的节点及其路径上的祖先节点。在访问这些节点时，如果需要下传标记（即访问子节点前），标记会被及时下传和清除，确保查询到的数据是包含所有未决更新的最新数据。未被查询区间覆盖的节点上的懒标记不会被触发，也不需要被清除以完成这次查询。
    *   **更新：** 当执行一个新的更新操作时，它可能会访问到之前带有懒标记的节点。在访问这些节点的子节点之前，会先下传并清除它们原有的懒标记（将旧更新应用到子节点），然后再处理新的更新（可能产生新的懒标记）。这确保了更新的顺序性和正确性。
    *   **关键点：** 只要后续操作访问到一个节点并需要进入其子节点，该节点上挂着的懒标记（无论来自多久之前的更新）都会被下传并清除。未被访问的节点上的懒标记则被安全地忽略。

**总结：**

线段树中的懒标记**不会**在程序结束时或某个特定时刻被全局清除。它们的清除是**按需**发生的：

*   **会被清除的标记：** 在后续的查询或更新操作中被访问到（并且需要递归到其子节点）的那些节点上的懒标记。在访问子节点之前，它们会被下传并清除。
*   **可能不会被清除的标记：** 那些在其生命周期内**从未被任何后续查询或更新操作访问过**的节点上的懒标记。这些标记会一直保留在节点上，但它们不会影响任何操作的正确性，因为它们关联的数据不再被需要。

因此，回答你的问题：**不是所有懒标记都会被清除**。只有那些后续操作触及到的节点上的懒标记才会被清除。未被触及的节点上的懒标记会一直存在，但这符合懒加载的设计原则且不影响正确性。









# 语法规则

## 1.typedef

typedef long long 别名

## 3.字典的用法：

![image-20250124201955858](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250124201955858.png)

如果 `a` 在 `map` 中不存在，`mp1[a]` 会自动创建一个空的 `vector<int>`，然后将 `b` 添加进去。

## 4.set的作用：

multiset允许元素重复

![2e1fd37b8d64a965d5c89b8d04ea724b_720](C:\Users\hp\Documents\Tencent Files\1759751014\nt_qq\nt_data\Pic\2025-01\Thumb\2e1fd37b8d64a965d5c89b8d04ea724b_720.jpg)

![c6bc0a28b6453a3b4f0bcc072887b2f0_720](C:\Users\hp\Documents\Tencent Files\1759751014\nt_qq\nt_data\Pic\2025-01\Thumb\c6bc0a28b6453a3b4f0bcc072887b2f0_720.jpg)

## 5.int最大保存10的9次方

2的正负31次方

## 6.参数数据类型

在C++中，如果函数参数类型为`long long`，实际传参可以传`int`类型的值。这是因为C++支持隐式类型转换，当传递一个`int`类型的参数给`long long`类型的参数时，编译器会自动将`int`类型转换为`long long`类型，这被称为整型提升。

需要注意的是，如果`int`类型的值超出了`long long`类型的表示范围，虽然转换仍会发生，但可能导致数据丢失或溢出，从而产生未定义的行为。因此，在传递参数时，应确保参数值在目标类型的有效范围内，以保证程序的正确性和可靠性。

## 7.排序

### 1.sort的降序排序

sort(vec.begin(), vec.end(), greater<int>());
// 结果：5, 4, 3, 2, 1

### 2.对数组排序

![image-20250307235522746](../AppData/Roaming/Typora/typora-user-images/image-20250307235522746.png)

### 3.vector<pair<int,int>>  v排序

```cpp
    // 按第二个元素排序
    sort(v.begin(), v.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.second < b.second;
    });

    // 输出结果
    for (const auto& p : v) {
        cout << "(" << p.first << ", " << p.second << ") ";
    }
    // 输出：(2, 1) (3, 1) (3, 2) (1, 4)
```





```cpp
    vector<pair<int, int>> v = {{3, 2}, {1, 4}, {2, 1}, {3, 1}};

    // 默认排序（按字典序）
    sort(v.begin(), v.end());

    // 输出结果
    for (const auto& p : v) {
        cout << "(" << p.first << ", " << p.second << ") ";
    }
    // 输出：(1, 4) (2, 1) (3, 1) (3, 2)
```

### 4.自定义比较大小

bool cmp(const pr& a, const pr& b) {
    if(a.sum != b.sum) return a.sum < b.sum;
    else return a.P > b.P; // sum相同时按P降序
}

- 该函数实现了 **先按 `sum` 升序，`sum` 相同时按 `P` 降序** 的排序规则。





## 8.设置某给定位数的小数

**必须要fixed和setprecision同时存在**

cout << fixed << setprecision(3) << 1.2345 << endl; // 1.235
cout << setprecision(0) << 5.678 << endl; // 6（四舍五入到整数）

## 9.数组当参数

void dfs(int* arr)

## 10.数组大小

![image-20250330170733632](../AppData/Roaming/Typora/typora-user-images/image-20250330170733632.png)

## 11.vector删除元素

如果删除的是`vector`中间的某个元素，那么所有在该元素之后的元素都需要向前移动一位来填补空缺，因此时间复杂度为O(n)，其中n是`vector`的长度。如果删除的是`vector`末尾的元素，那么时间复杂度为O(1)，因为不需要移动其他元素。

**删除一个元素**

#include <vector>
#include <algorithm>  // 需要包含 algorithm 以使用 find

using namespace std;

vector<int> vec = {1, 2, 3, 4, 5};

// 删除第3个元素（索引2）
auto it = vec.begin() + 2;
vec.erase(it); // vec变为 {1, 2, 4, 5}

// 删除第一个值为3的元素
auto it = find(vec.begin(), vec.end(), 3);
if (it != vec.end()) {
    vec.erase(it);
}

**删除多个元素**

#include <vector>

using namespace std;

vector<int> vec = {1, 2, 3, 4, 5};

// 删除第2到第4个元素（索引1到3）
vec.erase(vec.begin() + 1, vec.begin() + 4); // vec变为 {1, 5}

## 12.set和unordered_map的用法

在 C++ 中，`unordered_map` 和 `set` 是两个非常常用的容器，分别用于存储键值对和不重复的元素集合。下面我会详细讲解这两个容器及它们的用途。

### 1. `unordered_map<int, int> count;`

`unordered_map` 是一个哈希表（hash table），它以 **键值对** (`key-value pairs`) 的形式存储数据。它的主要特点是 **平均时间复杂度为 O(1)**，即查找、插入和删除操作的时间复杂度平均为常数级别。

- **int** 作为键 (`key`)，表示我们存储的项的唯一标识符。
- **int** 作为值 (`value`)，表示与键相关联的数据。

在你的代码中，`unordered_map<int, int> count;` 用来计数某些元素出现的频率。`count[key]` 将返回 `key` 对应的值。如果 `key` 不存在，它会自动插入并将其值初始化为 `0`，然后可以更新它。

**示例：**

```
cpp复制编辑unordered_map<int, int> count;
count[5]++;  // 如果键 5 存在，计数器加 1；如果不存在，自动初始化为 0 后再加 1
cout << count[5];  // 输出 1
```





还有种说法

`mp.count(j)` **检查键 `j` 是否存在于哈希映射 `mp` 中**：

- 如果存在，返回 `1`（因为 `unordered_map` 的键唯一）
- 如果不存在，返回 `0`



### 2. `set<int> result;`

`set` 是一个集合（Set）容器，它只存储 **唯一的元素**，并且会自动按元素大小排序。**元素不能重复**，如果尝试插入重复元素，`set` 会忽略它。

在你的代码中，`set<int> result;` 用来存储符合条件的 **唯一 ID**。由于 `set` 自动排序，因此它能够确保 `result` 中的 ID 是按升序排列的。

**示例：**

```
cpp复制编辑set<int> result;
result.insert(5);  // 插入 5
result.insert(3);  // 插入 3
result.insert(5);  // 插入重复的 5（会被忽略）

// 输出结果：3 5
for (int id : result) {
    cout << id << " ";
}
```

### 3.他们的erase操作

erase操作平均时间复杂度是O(1)

emplace操作也是O(1)



## 13.cstring里的小技巧

函数原型cpp复制void* memcpy(void* dest, const void* src, size_t count);
参数说明1.  dest ：目标内存区域的指针。2.  src ：源内存区域的指针。3.  count ：要复制的字节数。返回值返回目标内存区域的指针（即  dest ）。使用场景 memcpy  通常用于复制数组、结构体或其他内存块。它按字节逐个复制数据，不考虑数据类型。示例代码cpp复制#include <iostream>
#include <cstring> // 包含 memcpy 的头文件

int main() {
    int src[] = {1, 2, 3, 4, 5};
    int dest[5];

    // 使用 memcpy 复制 src 到 dest
    memcpy(dest, src, sizeof(src));
    
    // 输出 dest 的内容
    for (int i = 0; i < 5; i++) {
        std::cout << dest[i] << " ";
    }
    
    return 0;

}
输出复制1 2 3 4 5





int l=strlen(s1);**算的是长度**



**原地取反**

 cin>>s1;

 int l=strlen(s1);

 memcpy(s2,s1,l);

 reverse(s2,s2+l);





**string a=string b是深拷贝**



**string有个默认初始化**







## 14.子串与子序列



**子串：连续的字符序列，顺序必须与原字符串一致。**

**子序列：按原有顺序选取的字符序列，可以不连续。**



## 15.基本数据类型都是深拷贝

## 16.vector a=b是深拷贝

## 17.v.back()函数

取最后一个元素



# 解题技巧

## 1.区间

### 1.涉及到某些区间的边界效应

**可以把区间设置成左开右闭**（少取一点）

### 2.注意线段树的离散化

排下序就行

## 2.图

### 1.怎么样存下所有可能的图，并且去重

1.**这里的图是真的坐标系上的图！！！**

2.图用结构体的点(x,y)排序后的vector去存，并且要用set，如**set<vector<dot>> ans;**

3.注意要统一把所有图的左上点或其他标记点存在坐标原点

4.注意这里，如下，可快速转化成set对象

void dfs(vector<dot> g, ll w) {
    // 标准化并加入 ans
    dq(g);
    ans.insert(g);
    if (w == 0) return;  // 已添加完 k 个点

    // 枚举 g 中每个点的 4 个相邻位置
    set<dot> memo(g.begin(), g.end());

5.注意set里的count方法

for (dot t : g) {
        for (int i = 0; i < 4; i++) {
            dot nxt = {t.x+xx[i], t.y+yy[i]};
            **if (memo.count(nxt)) continue; // 已有点**
            vector<dot> tmp = g;
            tmp.push_back(nxt);
            dq(tmp);
            if (check(tmp)) {
                dfs(tmp, w-1);
            }
        }
    }
}

6.坐标系的旋转90°算法

struct dot {
    ll x, y;
    bool operator<(const dot& tmp) const {
        return x != tmp.x ? x < tmp.x : y < tmp.y;
    }
    // 顺时针旋转 90°
    void xz() { ll tx = x, ty = y; x = ty; y = -tx; }
    // 垂直翻转（关于 x 轴）
    void fx() { y = -y; }
    // 水平翻转（关于 y 轴）
    void fy() { x = -x; }
};

**7.这里最重要的是dfs的一种在原基础上搜索的方法**

原有的方格图，先用数列存下所有方格，对每个方格上下左右判断是否是否在数列中（set方法），如果在数列中，不加入，否则，递归地加入。

    void dfs(vector<dot> g, ll w) {
        // 1. 标准化当前点集，并加入结果集合 ans
        dq(g);
        ans.insert(g);
    
    // 2. 递归终止：已经添加完 w == k 次新点
    if (w == 0) return;
    
    // 3. 准备一个集合 memo，快速判断某个坐标是否已在 g 中
    set<dot> memo(g.begin(), g.end());
    
    // 4. 枚举当前图形 g 中每一个点 t，以及它的四个邻居位置
    for (dot t : g) {
        for (int i = 0; i < 4; i++) {
            dot nxt = { t.x + xx[i], t.y + yy[i] };
    
            // 4.1 如果邻居位置已被占用，就跳过
            if (memo.count(nxt)) continue;
    
            // 4.2 否则在 g 的拷贝 tmp 上“添加”这个新点 nxt
            vector<dot> tmp = g;
            tmp.push_back(nxt);
    
            // 4.3 标准化 tmp（对齐到原点并排序），然后判重
            dq(tmp);
            if (check(tmp)) {
                // 4.4 如果是“新”形状，就继续往下递归，剩余可添加次数减 1
                dfs(tmp, w - 1);
            }
        }
    }
}

### 2.存图的边关系可以用unordered_map

**if (visited.find(node) != visited.end()) 用这个函数判断他是否找到了那条边**



## 3.二进制

### 1.二进制移位

**注意负数不行，仅限正数**





```cpp
	inline int ls(int p){return p<<1;}//左儿子 
	inline int rs(int p){return p<<1|1;}//右儿子 
```



1、此处的 `inline` 可以有效防止无需入栈的信息入栈，节省时间和空间。

2、二进制位左移一位代表着数值 ×2，而如果左移完之后再或上 1，由于左移完之后最后一位二进制位上一定会是 0 ，所以 ∣1 等价于 +1 。



int result = num >> 1; // 等价于 num / 2（向下取整）

### 2.如何在二进制中减去最后一个1

直接进行(x-1)&x操作

### 3.自己在二进制运算中要懂得构建特殊二进制串

如1010101010









## 4.状态压缩

**状态压缩**是一种优化技术，通过高效的数据表示方式减少内存占用并提升计算效率，常用于处理包含多个状态的问题。以下是其核心要点：

### 核心概念

1. **状态的高效表示**：
   - 将复杂状态（如集合、布尔数组）压缩为更简洁的形式（如整数、位掩码）。
   - **示例**：用二进制位表示元素是否存在（如`1010`表示第1、3个元素被选中）。

2. **优化目标**：
   - **减少内存消耗**：避免使用高维数组或多变量存储。
   - **加速状态操作**：位运算比遍历数组更高效。

---

### 典型应用场景

1. **动态规划（DP）**：
   - **空间优化**：当状态转移仅依赖前几个状态时，压缩存储维度。例如斐波那契数列只需保存前两个值，而非整个数组。
   - **集合表示**：如旅行商问题（TSP）中，用位掩码表示已访问的城市集合，状态`dp[i][mask]`压缩为整数`mask`。

2. **搜索算法（BFS/DFS）**：
   - **状态哈希**：将棋盘布局、节点访问情况压缩为整数，便于快速查重和存储。例如八皇后问题用位掩码标记列和对角线冲突。

3. **位运算优化**：
   - **快速判断与更新**：用位操作代替条件判断。例如检查第`i`位是否为1：`mask & (1 << i)`；设置第`i`位：`mask |= (1 << i)`。

---

### 实例说明

- **旅行商问题（TSP）**：
  - 状态定义：`dp[mask][i]`表示通过城市集合`mask`（二进制位表示）到达城市`i`的最短路径。
  - 压缩优势：用1个整数替代数组存储，节省空间且支持快速位运算。

- **棋盘类问题**：
  - 如八皇后、数独，用位掩码标记行、列、对角线的占用情况，避免多层循环检查冲突。

---

### 注意事项

- **位数限制**：32/64位整数的位掩码最多表示32/64个元素的状态，超规模问题需分块或其他方法。
- **可读性**：位操作可能降低代码可读性，需适当注释或封装函数。

---

### 总结

状态压缩通过**位掩码**、**简化状态维度**等方式，将复杂状态转化为紧凑的数值形式，显著优化内存与计算效率。适用于动态规划、搜索及需要高效集合操作的场景，是处理中等规模组合问题的有效手段。





## 5.记忆化搜索

### 什么时候使用（说人话版）

而不同的插入球的顺序，也可能得到相同的状态。因此，如果使用深度优先搜索，则需要使用记忆化搜索，以避免重复计算相同的状态。

### 简介

**记忆化搜索（Memoization Search）**是一种结合递归与缓存技术的优化方法，核心思想是通过记录已计算过的子问题结果，避免重复计算，从而显著提升算法效率。其本质是**“用空间换时间”**，常用于动态规划或递归问题的优化。

---

### **核心概念**

1. **缓存机制**：
   - 在递归过程中，将每个子问题的计算结果存储到缓存（如数组、哈希表），下次遇到相同子问题时直接读取结果，而非重新计算。
   - **关键点**：仅对存在重复子问题的场景有效。

2. **自顶向下（Top-Down）**：
   - 从原问题出发，逐步分解为子问题，通过递归解决子问题并缓存结果。
   - 与动态规划（自底向上）互补，但思维模式更贴近递归的自然逻辑。

---

### **典型应用场景**

1. **递归中的重复子问题**：

   - 例如斐波那契数列：`F(n) = F(n-1) + F(n-2)`，直接递归的时间复杂度为 `O(2^n)`，而记忆化可优化至 `O(n)`。

   - **代码示例（Python）**：

     ```python
     memo = {}
     def fib(n):
         if n in memo: return memo[n]  # 查缓存
         if n <= 1: return n
         res = fib(n-1) + fib(n-2)
         memo[n] = res  # 存缓存
         return res
     ```

2. **动态规划的递归实现**：

   - 如背包问题、最短路径问题，用递归+记忆化代替迭代填表，降低实现难度。
   - **示例**：LeetCode 的爬楼梯问题（每次爬1或2阶，求到顶的方案数）。

3. **复杂状态转移问题**：

   - 如棋盘路径搜索（国际象棋中的骑士遍历）、数独求解，通过缓存已探索的状态剪枝。

---

### **记忆化搜索 vs. 动态规划（DP）**

| **特性**     | **记忆化搜索**               | **动态规划**                 |
| ------------ | ---------------------------- | ---------------------------- |
| **方向**     | 自顶向下（从问题到子问题）   | 自底向上（从子问题到原问题） |
| **实现方式** | 递归 + 缓存                  | 迭代填表                     |
| **空间控制** | 仅缓存必要结果，可能更省空间 | 通常需存储所有子问题的结果   |
| **适用场景** | 子问题结构复杂或稀疏分布     | 子问题明确且需全局遍历       |
| **可读性**   | 更贴近问题自然逻辑           | 需设计状态转移方程           |

---

### **优缺点**

- **优点**：
  - **实现简单**：仅需在递归基础上添加缓存逻辑。
  - **避免冗余计算**：尤其适合子问题重复率高的问题。
  - **灵活控制计算顺序**：按需计算，避免处理无用状态。

- **缺点**：
  - **递归深度限制**：可能导致栈溢出（如Python默认递归深度约1000层）。
  - **额外空间开销**：需存储缓存结构。
  - **无法优化计算顺序**：依赖递归调用，可能不如DP迭代高效。

---

### **实例说明**

#### 1. **斐波那契数列**

- **原始递归**：计算 `fib(5)` 需要重复计算 `fib(2)`、`fib(3)` 多次。
- **记忆化后**：每个 `fib(n)` 仅计算一次，后续直接查表。

#### 2. **LeetCode 62. 不同路径**

- **问题**：从网格左上角到右下角的路径数（每次只能右或下移）。

- **记忆化实现**：

  ```python
  memo = {}
  def unique_paths(m, n):
      if (m, n) in memo: return memo[(m, n)]
      if m == 1 or n == 1: return 1
      res = unique_paths(m-1, n) + unique_paths(m, n-1)
      memo[(m, n)] = res
      return res
  ```

- **时间复杂度**：从 `O(2^(m+n))` 优化至 `O(m*n)`。

---

### **总结**

记忆化搜索是**递归的自然优化延伸**，通过缓存子问题结果将指数级复杂度降为多项式级。它特别适合子问题重叠度高、状态转移复杂或难以直接设计DP填表顺序的问题，是动态规划的“递归版本”，也是算法竞赛和面试中的高频优化手段。

## 6.双指针

双指针重要的是要有数学规律，才能用

## 7.最值的搜索——bfs

bfs非常擅长搜索最小值
