# 学习 Supabase 的过滤器

在上一篇文章中，我们通过 Python SDK 实现了 Supabase 数据库的增删改查，在查询、修改和删除数据时，我们使用了类似于 `eq` 和 `in_` 这样的过滤方法，这被称为 **过滤器（filters）**。

![](./images/supabase-filters.jpg)

Supabase 提供了丰富的过滤器，可以满足各种需求，今天我们来详细了解一下 Supabase 的过滤器。

## 基本用法

下面是 Supabase Python SDK 中的过滤器的基本用法：

```python
response = (
    supabase.table("students")
    .select("*")
    .eq("name", "zhangsan")
    .execute()
)
```

Supabase 常用的过滤器包括：

| 过滤器 | 描述 | 示例 |
| --- | --- | --- |
| eq | 等于 | `.eq("id", 15)` |
| neq | 不等于 | `.neq("id", 15)` |
| gt | 大于 | `.gt("age", 18)` |
| gte | 大于等于 | `.gte("age", 18)` |
| lt | 小于 | `.lt("age", 18)` |
| lte | 小于等于 | `.lte("age", 18)` |
| like | 模糊匹配 | `.like("name", "zhang%")` |
| ilike | 模糊匹配，不区分大小写 | `.ilike("name", "zhang%")` |
| is_ | 是否满足某种条件，比如是否为 NULL | `.is_("name", "null")` |
| not_ | 对某个过滤器取反 | `.not_.is_("name", "null")` |
| in_ | 在列表中 | `.in_("id", [1, 2, 3])` |

## 范围列和数组列

在 Supabase 中，范围列用于存储数值范围，这种类型的列可以表示一个区间，例如 [1, 10] 表示从 1 到 10 的范围；数组列用于存储数组，例如 [1, 2, 3] 表示一个数组。我们创建一个示例表，包括范围列和数组列：

```sql
CREATE TABLE examples (
    id SERIAL PRIMARY KEY,
    range_column INT4RANGE, -- 范围列
    array_column INT[] -- 数组列
);
```

并开启 RLS：

```sql
ALTER TABLE examples
ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all access"
ON "public"."examples"
FOR ALL
USING (true);
```

然后插入几条示例数据：

```python
response = (
    supabase.table("examples")
    .insert([
        {"range_column": [1, 5], "array_column": [1, 2, 3, 4, 5]},
        {"range_column": [6, 10], "array_column": [6, 7, 8, 9, 10]},
    ])
    .execute()
)
```

范围列和数组列支持一些特殊的过滤器，包括：

| 过滤器 | 描述 | 示例 |
| --- | --- | --- |
| contains | 数组中包含所有元素 | `.contains("array_column", ["1", "2", "3"])` |
| contained_by | 数组中所有元素被包含 | `.contained_by("array_column", ["1", "2", "3", "4", "5", "6"])` |
| range_gt | 范围大于，所有元素都大于范围内的值 | `.range_gt("range_column", [1, 5])` |
| range_gte | 范围大于等于，所有元素都大于等于范围内的值 | `.range_gte("range_column", [1, 5])` |
| range_lt | 范围小于，所有元素都小于范围内的值 | `.range_lt("range_column", [6, 10])` |
| range_lte | 范围小于等于，所有元素都小于等于范围内的值 | `.range_lte("range_column", [6, 10])` |
| range_adjacent | 范围相邻且互斥 | `.range_adjacent("range_column", [10, 15])` |
| overlaps | 数组中含有重叠元素 | `.overlaps("array_column", ["1", "3", "5"])` |

## JSON 列

Supabase 支持 JSON 列，可以存储 JSON 格式的数据，JSON 列有两种类型：

* JSON - 作为字符串存储
* JSONB - 作为二进制存储

在几乎所有情况下，推荐使用 JSONB 类型，我们创建一个示例表，包括 JSONB 列：

```sql
CREATE TABLE examples2 (
    id SERIAL PRIMARY KEY,
    json_column JSONB
);
```

和之前一样，开启 RLS：

```sql
ALTER TABLE examples2
ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all access"
ON "public"."examples2"
FOR ALL
USING (true);
```

然后插入几条示例数据：

```python
response = (
    supabase.table("examples2")
    .insert([
        {"json_column": {"name": "zhangsan", "age": 15}},
        {"json_column": {"name": "lisi", "age": 16}},
    ])
    .execute()
)
```

我们可以在查询时，使用 `->` 操作符来获取 JSON 中的某个字段：

```python
response = (
    supabase.table("examples2")
    .select("id, json_column->name, json_column->age")
    .execute()
)
```

我们也可以在过滤器中使用 `->` 操作符：

```python
response = (
    supabase.table("examples2")
    .select("*")
    .eq("json_column->age", 15)
    .execute()
)
```

如果要过滤的字段值是字符串类型，可以使用 `->>` 操作符：

```python
response = (
    supabase.table("examples2")
    .select("*")
    .eq("json_column->>name", "zhangsan")
    .execute()
)
```

## 复合过滤器

Supabase 支持复合过滤器，可以将多个过滤器组合在一起，比如：

```python
response = (
    supabase.table("students")
    .select("*")
    .gt("age", 15)
    .lt("age", 18)
    .execute()
)
```

这个表示 age 大于 15 且小于 18 的数据，如果要表示 age 小于等于 15 或者大于等于 18 的数据，可以使用 `or_` 过滤器：

```python
response = (
    supabase.table("students")
    .select("*")
    .or_("age.lte.15,age.gte.18")
    .execute()
)
```

`or_` 过滤器的参数是一个字符串，使用的是原始的 PostgREST 语法，格式为 `column.operator.value`，多个过滤器之间用逗号分隔。

当我们希望同时匹配多个字段时，可以使用 `match` 过滤器：

```python
response = (
    supabase.table("students")
    .select("*")
    .match({"age": 15, "name": "zhangsan"})
    .execute()
)
```

这个表示 age 等于 15 且 name 等于 zhangsan 的数据，`match` 和多个 `eq` 是等价的：

```python
response = (
    supabase.table("students")
    .select("*")
    .eq("age", 15)
    .eq("name", "zhangsan")
    .execute()
)
```
