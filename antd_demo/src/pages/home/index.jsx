import { Card, Col, Form, List, Row, Select, Typography, Tag, Icon } from 'antd';
import React, { Component } from 'react';
import { connect } from 'dva';
import moment from 'moment';
import { range } from 'lodash';

import AvatarList from './components/AvatarList';
import StandardFormRow from './components/StandardFormRow';
import styles from './style.less';

const { Option } = Select;
const FormItem = Form.Item;
const { Paragraph } = Typography;

class Home extends Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'home/fetch',
      payload: {
        count: 8,
      },
    });
  }

  getHeader = () => (
    <div className={styles.homeHeader}>
      <h2>学习中心</h2>
      <p>文案待定</p>
    </div>
  );

  getVideos = () => {
    const {
      home: { list = [] },
      loading,
    } = this.props;
    return list ? (
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
        dataSource={list.slice(0, 4)}
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
  };

  getVideoList = (type) => {
    const title = type.split("").join(" / ");
    return (
      <div className={styles.coverCardList}>
        <h2>{title}</h2>
        <hr />
        <div className={styles.cardList}>{this.getVideos()}</div>
      </div>
    )
  };

  getHotVideoList = () => {
    const {
      home: { list = [] },
      loading,
    } = this.props;
    return list.slice(3, 8).map((item) => (
      <Card
        className={styles.card}
        hoverable
        cover={<img alt={item.title} src={item.cover} />}
      >
        <Card.Meta
          title={item.title}
        />
      </Card>
    ));
  }

  render() {
    const videoTypes = ['新手入门', '技能提升', '实战推荐'];
    return (
      <div className={styles.home}>
        {this.getHeader()}
        <div className={styles.homeMain}>
          <div className={styles.homeLeft}>
            <div className={styles.homeVideo}>
              <div className={styles.mainTitle}>
                视频学习
              </div>
              { 
                videoTypes.map((item) => this.getVideoList(item))
              }
            </div>
            <div className={styles.homeArticle}>
              <div className={styles.mainTitle}>
                入门文档
              </div>
              { 
                this.getVideoList("")
              }
            </div>
          </div>
          <div className={styles.homeRight}>
            <div className={styles.hotVideos}>
              <div className={styles.hotVideoTitle}>
                热门视频
              </div>
              <div className={styles.hotVideoList}>
                {
                  this.getHotVideoList()
                }
              </div>
            </div>
          </div>
        </div>
      
      </div>
      
    );
  }
}

const WarpForm = Form.create({
  onValuesChange({ dispatch }) {
    // 表单项变化时请求数据
    // 模拟查询表单生效
    dispatch({
      type: 'home/fetch',
      payload: {
        count: 8,
      },
    });
  },
})(Home);
export default connect(({ home, loading }) => ({
  home: home,
  loading: loading.models.home,
}))(WarpForm);
