import { Card, Col, Form, List, Row, Select, Typography, Tag, Icon } from 'antd';
import React, { Component } from 'react';
import { connect } from 'dva';
import moment from 'moment';
import AvatarList from './components/AvatarList';
import StandardFormRow from './components/StandardFormRow';
import TagSelect from './components/TagSelect';
import styles from './style.less';

const { Option } = Select;
const FormItem = Form.Item;
const { Paragraph } = Typography;

class Videos extends Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'videos/fetch',
      payload: {
        count: 8,
      },
    });
  }

  render() {
    const {
      videos: { list = [] },
      loading,
      form,
    } = this.props;
    const { getFieldDecorator } = form;
    const cardList = list ? (
      <List
        rowKey="id"
        loading={loading}
        grid={{
          gutter: 24,
          xl: 4,
          lg: 3,
          md: 3,
          sm: 2,
          xs: 1,
        }}
        dataSource={list}
        renderItem={item => (
          <List.Item>
            <Card
              className={styles.card}
              hoverable
              cover={<img alt={item.title} src={item.cover} />}
            >
              <Card.Meta
                title={item.title}
                description={
                  <div className={styles.cardDesc}>
                    <Tag>
                      {item.type}
                    </Tag>
                    <div className={styles.cardView}>
                      <Icon type="eye" />
                      {item.count}
                    </div>
                  </div>
                }
              />
            </Card>
          </List.Item>
        )}
      />
    ) : null;
    const formItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
        },
        sm: {
          span: 16,
        },
      },
    };
    return (
      <div className={styles.coverCardList}>
        <Card bordered={false}>
          <Form layout="inline">
            <StandardFormRow
              title="所属类目"
              block
              style={{
                paddingBottom: 11,
              }}
            >
              <FormItem>
                {getFieldDecorator('category')(
                  <TagSelect>
                    <TagSelect.Option value="cat1">CI / CD</TagSelect.Option>
                    <TagSelect.Option value="cat2">k8s</TagSelect.Option>
                    <TagSelect.Option value="cat3">DevOps</TagSelect.Option>
                    <TagSelect.Option value="cat4">GitOps</TagSelect.Option>
                    <TagSelect.Option value="cat5">Istio</TagSelect.Option>
                    <TagSelect.Option value="cat6">Promethues</TagSelect.Option>
                  </TagSelect>,
                )}
              </FormItem>
            </StandardFormRow>
            {/* <StandardFormRow title="其它选项" grid last>
              <Row gutter={16}>
                <Col lg={8} md={10} sm={10} xs={24}>
                  <FormItem {...formItemLayout} label="作者">
                    {getFieldDecorator('author', {})(
                      <Select
                        placeholder="不限"
                        style={{
                          maxWidth: 200,
                          width: '100%',
                        }}
                      >
                        <Option value="lisa">王昭君</Option>
                      </Select>,
                    )}
                  </FormItem>
                </Col>
                <Col lg={8} md={10} sm={10} xs={24}>
                  <FormItem {...formItemLayout} label="好评度">
                    {getFieldDecorator('rate', {})(
                      <Select
                        placeholder="不限"
                        style={{
                          maxWidth: 200,
                          width: '100%',
                        }}
                      >
                        <Option value="good">优秀</Option>
                        <Option value="normal">普通</Option>
                      </Select>,
                    )}
                  </FormItem>
                </Col>
              </Row>
            </StandardFormRow> */}
          </Form>
        </Card>
        <div className={styles.cardList}>{cardList}</div>
      </div>
    );
  }
}

const WarpForm = Form.create({
  onValuesChange({ dispatch }) {
    // 表单项变化时请求数据
    // 模拟查询表单生效
    dispatch({
      type: 'videos/fetch',
      payload: {
        count: 8,
      },
    });
  },
})(Videos);
export default connect(({ videos, loading }) => ({
  videos,
  loading: loading.models.videos,
}))(WarpForm);
