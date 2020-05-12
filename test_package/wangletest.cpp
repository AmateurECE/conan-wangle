#include <wangle/bootstrap/ServerBootstrap.h>
#include <wangle/bootstrap/ClientBootstrap.h>
#include <wangle/channel/Handler.h>

#include <boost/thread.hpp>
#include <folly/String.h>

using namespace wangle;
using namespace folly;

typedef Pipeline<IOBufQueue&, std::unique_ptr<IOBuf>> BytesPipeline;
typedef ServerBootstrap<BytesPipeline> TestServer;

class TestPipelineFactory : public PipelineFactory<BytesPipeline> {
 public:
  BytesPipeline::Ptr newPipeline(
      std::shared_ptr<AsyncTransportWrapper>) override {
    pipelines++;
    auto pipeline = BytesPipeline::create();
    pipeline->addBack(new BytesToBytesHandler());
    pipeline->finalize();
    return pipeline;
  }
  std::atomic<int> pipelines{0};
};

int main()
{
  TestServer server;
  server.childPipeline(std::make_shared<TestPipelineFactory>());
  server.bind(0);
  server.stop();
}
